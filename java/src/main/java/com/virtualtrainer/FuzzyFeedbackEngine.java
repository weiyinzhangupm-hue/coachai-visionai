package com.virtualtrainer;

import net.sourceforge.jFuzzyLogic.FIS;
import net.sourceforge.jFuzzyLogic.rule.Variable;

/**
 * 模糊反馈引擎
 * 使用JFuzzyLogic提供运动质量反馈
 */
public class FuzzyFeedbackEngine {
    
    private FIS fis;
    private String fclPath;
    
    /**
     * 构造函数
     */
    public FuzzyFeedbackEngine() {
        this.fclPath = "src/main/resources/fitness_feedback.fcl";
    }
    
    /**
     * 加载FCL模糊规则文件
     * 
     * @param fclPath FCL文件路径
     * @throws Exception 如果加载失败
     */
    public void loadFCL(String fclPath) throws Exception {
        this.fclPath = fclPath;
        fis = FIS.load(fclPath, true);
        
        if (fis == null) {
            throw new Exception("无法加载FCL文件: " + fclPath);
        }
        
        System.out.println("模糊规则加载成功: " + fclPath);
    }
    
    /**
     * 生成运动反馈
     * 
     * @param velocidad 速度（秒/次）
     * @param amplitud 幅度（角度）
     * @param estabilidad 稳定性（0-100）
     * @param fatiga 疲劳度（0-100）
     * @return 反馈结果对象
     * @throws Exception 如果推理失败
     */
    public FeedbackResult generateFeedback(double velocidad, double amplitud, 
                                           double estabilidad, double fatiga) throws Exception {
        if (fis == null) {
            loadFCL(fclPath);
        }
        
        // 设置输入变量
        fis.setVariable("velocidad", velocidad);
        fis.setVariable("amplitud", amplitud);
        fis.setVariable("estabilidad", estabilidad);
        fis.setVariable("fatiga", fatiga);
        
        // 执行推理
        fis.evaluate();
        
        // 获取输出
        Variable puntuacion = fis.getVariable("puntuacion");
        double score = puntuacion.getValue();
        
        // 生成反馈文本
        String feedbackText = generateFeedbackText(velocidad, amplitud, estabilidad, fatiga, score);
        
        // 生成建议
        String[] suggestions = generateSuggestions(velocidad, amplitud, estabilidad, fatiga);
        
        return new FeedbackResult(score, feedbackText, suggestions);
    }
    
    /**
     * 生成反馈文本
     */
    private String generateFeedbackText(double velocidad, double amplitud, 
                                        double estabilidad, double fatiga, double score) {
        StringBuilder feedback = new StringBuilder();
        
        // 根据评分给出总体评价
        if (score >= 8.0) {
            feedback.append("优秀！");
        } else if (score >= 6.0) {
            feedback.append("良好，");
        } else if (score >= 4.0) {
            feedback.append("尚可，");
        } else {
            feedback.append("需要改进，");
        }
        
        // 速度反馈
        if (velocidad < 1.5) {
            feedback.append("速度过快，");
        } else if (velocidad > 3.5) {
            feedback.append("速度较慢，");
        } else {
            feedback.append("速度合适，");
        }
        
        // 幅度反馈
        if (amplitud < 70) {
            feedback.append("幅度严重不足，");
        } else if (amplitud < 90) {
            feedback.append("幅度稍显不足，");
        } else if (amplitud >= 90 && amplitud <= 130) {
            feedback.append("幅度良好，");
        } else {
            feedback.append("幅度过大，");
        }
        
        // 稳定性反馈
        if (estabilidad < 60) {
            feedback.append("动作不够稳定");
        } else if (estabilidad < 80) {
            feedback.append("稳定性一般");
        } else {
            feedback.append("动作稳定");
        }
        
        // 疲劳提示
        if (fatiga > 60) {
            feedback.append("，建议休息");
        }
        
        return feedback.toString();
    }
    
    /**
     * 生成具体建议
     */
    private String[] generateSuggestions(double velocidad, double amplitud, 
                                         double estabilidad, double fatiga) {
        java.util.ArrayList<String> suggestions = new java.util.ArrayList<>();
        
        // 速度建议
        if (velocidad < 1.5) {
            suggestions.add("放慢动作速度，注重动作质量");
        } else if (velocidad > 3.5) {
            suggestions.add("可以适当加快节奏");
        }
        
        // 幅度建议
        if (amplitud < 90) {
            suggestions.add("增加动作幅度，蹲得更深/俯得更低");
        } else if (amplitud > 130) {
            suggestions.add("控制动作幅度，避免过度伸展");
        }
        
        // 稳定性建议
        if (estabilidad < 70) {
            suggestions.add("保持核心收紧，增强动作稳定性");
            suggestions.add("可以降低速度，专注于控制");
        }
        
        // 疲劳建议
        if (fatiga > 70) {
            suggestions.add("疲劳度较高，建议休息1-2分钟");
        } else if (fatiga > 50) {
            suggestions.add("注意调整呼吸节奏");
        }
        
        return suggestions.toArray(new String[0]);
    }
    
    /**
     * 获取模糊推理的详细信息（调试用）
     */
    public String getDetailedInfo() {
        if (fis == null) {
            return "模糊系统未初始化";
        }
        
        StringBuilder info = new StringBuilder();
        info.append("=== 模糊推理详细信息 ===\n");
        info.append(fis.toString());
        
        return info.toString();
    }
    
    /**
     * 反馈结果内部类
     */
    public static class FeedbackResult {
        private double score;
        private String feedbackText;
        private String[] suggestions;
        
        public FeedbackResult(double score, String feedbackText, String[] suggestions) {
            this.score = score;
            this.feedbackText = feedbackText;
            this.suggestions = suggestions;
        }
        
        public double getScore() {
            return score;
        }
        
        public String getFeedbackText() {
            return feedbackText;
        }
        
        public String[] getSuggestions() {
            return suggestions;
        }
        
        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            sb.append(String.format("评分: %.1f/10\n", score));
            sb.append("反馈: ").append(feedbackText).append("\n");
            sb.append("建议:\n");
            for (String suggestion : suggestions) {
                sb.append("  - ").append(suggestion).append("\n");
            }
            return sb.toString();
        }
        
        /**
         * 转换为JSON格式（用于API响应）
         */
        public String toJSON() {
            StringBuilder json = new StringBuilder();
            json.append("{");
            json.append("\"score\":").append(score).append(",");
            json.append("\"feedback_text\":\"").append(feedbackText).append("\",");
            json.append("\"suggestions\":[");
            for (int i = 0; i < suggestions.length; i++) {
                json.append("\"").append(suggestions[i]).append("\"");
                if (i < suggestions.length - 1) json.append(",");
            }
            json.append("]");
            json.append("}");
            return json.toString();
        }
    }
    
    /**
     * 主函数 - 测试用
     */
    public static void main(String[] args) {
        try {
            FuzzyFeedbackEngine engine = new FuzzyFeedbackEngine();
            
            // 测试用例1：优秀的动作
            System.out.println("=== 测试用例1：优秀动作 ===");
            FeedbackResult result1 = engine.generateFeedback(2.0, 110, 85, 20);
            System.out.println(result1);
            
            // 测试用例2：需要改进的动作
            System.out.println("\n=== 测试用例2：需改进动作 ===");
            FeedbackResult result2 = engine.generateFeedback(4.5, 75, 55, 70);
            System.out.println(result2);
            
            // 测试用例3：速度过快
            System.out.println("\n=== 测试用例3：速度过快 ===");
            FeedbackResult result3 = engine.generateFeedback(1.0, 100, 75, 30);
            System.out.println(result3);
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

