package com.virtualtrainer;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * 工具类
 * 提供通用辅助方法
 */
public class Utils {
    
    /**
     * 打印系统信息
     */
    public static void printSystemInfo() {
        System.out.println("=".repeat(60));
        System.out.println("系统信息");
        System.out.println("=".repeat(60));
        System.out.println("Java版本: " + System.getProperty("java.version"));
        System.out.println("操作系统: " + System.getProperty("os.name"));
        System.out.println("工作目录: " + System.getProperty("user.dir"));
        System.out.println("=".repeat(60));
    }
    
    /**
     * 确保目录存在
     * 
     * @param dirPath 目录路径
     * @return 目录是否存在或创建成功
     */
    public static boolean ensureDirectory(String dirPath) {
        File dir = new File(dirPath);
        if (!dir.exists()) {
            return dir.mkdirs();
        }
        return true;
    }
    
    /**
     * 获取当前时间戳字符串
     * 
     * @return 格式化的时间戳
     */
    public static String getTimestamp() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        return sdf.format(new Date());
    }
    
    /**
     * 获取文件扩展名
     * 
     * @param filename 文件名
     * @return 扩展名（不含点）
     */
    public static String getFileExtension(String filename) {
        int lastDot = filename.lastIndexOf('.');
        if (lastDot > 0 && lastDot < filename.length() - 1) {
            return filename.substring(lastDot + 1);
        }
        return "";
    }
    
    /**
     * 检查文件是否存在
     * 
     * @param filepath 文件路径
     * @return 文件是否存在
     */
    public static boolean fileExists(String filepath) {
        return new File(filepath).exists();
    }
    
    /**
     * 格式化字节大小
     * 
     * @param bytes 字节数
     * @return 格式化的字符串（如 "1.5 MB"）
     */
    public static String formatBytes(long bytes) {
        if (bytes < 1024) return bytes + " B";
        int exp = (int) (Math.log(bytes) / Math.log(1024));
        char pre = "KMGTPE".charAt(exp - 1);
        return String.format("%.1f %sB", bytes / Math.pow(1024, exp), pre);
    }
    
    /**
     * 打印进度条
     * 
     * @param current 当前进度
     * @param total 总数
     * @param barLength 进度条长度
     */
    public static void printProgressBar(int current, int total, int barLength) {
        double percentage = (double) current / total;
        int filled = (int) (barLength * percentage);
        
        StringBuilder bar = new StringBuilder("[");
        for (int i = 0; i < barLength; i++) {
            if (i < filled) {
                bar.append("=");
            } else if (i == filled) {
                bar.append(">");
            } else {
                bar.append(" ");
            }
        }
        bar.append("] ");
        bar.append(String.format("%.1f%%", percentage * 100));
        
        System.out.print("\r" + bar.toString());
        if (current == total) {
            System.out.println();
        }
    }
    
    /**
     * 计算数组的平均值
     * 
     * @param values 数值数组
     * @return 平均值
     */
    public static double average(double[] values) {
        if (values == null || values.length == 0) {
            return 0.0;
        }
        double sum = 0;
        for (double v : values) {
            sum += v;
        }
        return sum / values.length;
    }
    
    /**
     * 计算数组的标准差
     * 
     * @param values 数值数组
     * @return 标准差
     */
    public static double standardDeviation(double[] values) {
        if (values == null || values.length < 2) {
            return 0.0;
        }
        double avg = average(values);
        double sumSq = 0;
        for (double v : values) {
            sumSq += Math.pow(v - avg, 2);
        }
        return Math.sqrt(sumSq / values.length);
    }
    
    /**
     * 休眠指定毫秒数
     * 
     * @param millis 毫秒数
     */
    public static void sleep(long millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    /**
     * 主函数 - 测试工具方法
     */
    public static void main(String[] args) {
        printSystemInfo();
        
        System.out.println("\n测试工具方法:");
        System.out.println("时间戳: " + getTimestamp());
        System.out.println("格式化字节: " + formatBytes(1536000));
        
        System.out.println("\n进度条演示:");
        for (int i = 0; i <= 100; i++) {
            printProgressBar(i, 100, 50);
            sleep(20);
        }
        
        double[] testData = {1.5, 2.3, 3.1, 2.8, 3.5};
        System.out.println("\n统计测试:");
        System.out.println("平均值: " + average(testData));
        System.out.println("标准差: " + standardDeviation(testData));
    }
}

