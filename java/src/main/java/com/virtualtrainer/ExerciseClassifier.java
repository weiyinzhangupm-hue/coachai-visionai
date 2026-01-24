package com.virtualtrainer;

import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.classifiers.Classifier;
import weka.classifiers.trees.J48;
import weka.classifiers.bayes.NaiveBayes;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

/**
 * 运动分类器类
 * 使用Weka进行运动动作分类
 */
public class ExerciseClassifier {
    
    private Classifier classifier;
    private Instances dataStructure;
    
    /**
     * 加载训练好的模型
     * 
     * @param modelPath 模型文件路径
     * @throws Exception 如果加载失败
     */
    public void loadModel(String modelPath) throws Exception {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(modelPath));
        classifier = (Classifier) ois.readObject();
        ois.close();
        System.out.println("模型加载成功: " + modelPath);
    }
    
    /**
     * 训练新模型
     * 
     * @param dataPath 训练数据路径（ARFF或CSV）
     * @param modelType 模型类型（"J48"或"NaiveBayes"）
     * @throws Exception 如果训练失败
     */
    public void trainModel(String dataPath, String modelType) throws Exception {
        // 加载数据
        DataSource source = new DataSource(dataPath);
        Instances data = source.getDataSet();
        
        // 设置类别属性（最后一列）
        if (data.classIndex() == -1) {
            data.setClassIndex(data.numAttributes() - 1);
        }
        
        this.dataStructure = new Instances(data, 0);
        
        // 创建分类器
        if (modelType.equalsIgnoreCase("J48")) {
            classifier = new J48();
        } else if (modelType.equalsIgnoreCase("NaiveBayes")) {
            classifier = new NaiveBayes();
        } else {
            throw new Exception("未知的模型类型: " + modelType);
        }
        
        // 训练模型
        System.out.println("开始训练模型...");
        classifier.buildClassifier(data);
        System.out.println("模型训练完成");
    }
    
    /**
     * 分类新实例
     * 
     * @param features 特征数组
     * @return 分类结果对象
     * @throws Exception 如果分类失败
     */
    public ClassificationResult classify(double[] features) throws Exception {
        if (classifier == null) {
            throw new Exception("模型未加载，请先加载或训练模型");
        }
        
        // 创建实例
        weka.core.DenseInstance instance = new weka.core.DenseInstance(features.length);
        instance.setDataset(dataStructure);
        
        for (int i = 0; i < features.length - 1; i++) {
            instance.setValue(i, features[i]);
        }
        
        // 进行分类
        double classValue = classifier.classifyInstance(instance);
        double[] distribution = classifier.distributionForInstance(instance);
        
        // 获取类别名称
        String className = dataStructure.classAttribute().value((int) classValue);
        double confidence = distribution[(int) classValue];
        
        return new ClassificationResult(className, confidence, distribution);
    }
    
    /**
     * 保存模型
     * 
     * @param modelPath 模型保存路径
     * @throws Exception 如果保存失败
     */
    public void saveModel(String modelPath) throws Exception {
        ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(modelPath));
        oos.writeObject(classifier);
        oos.close();
        System.out.println("模型已保存: " + modelPath);
    }
    
    /**
     * 评估模型性能
     * 
     * @param testDataPath 测试数据路径
     * @throws Exception 如果评估失败
     */
    public void evaluateModel(String testDataPath) throws Exception {
        DataSource source = new DataSource(testDataPath);
        Instances testData = source.getDataSet();
        testData.setClassIndex(testData.numAttributes() - 1);
        
        weka.classifiers.Evaluation eval = new weka.classifiers.Evaluation(testData);
        eval.evaluateModel(classifier, testData);
        
        System.out.println("=== 模型评估结果 ===");
        System.out.println(eval.toSummaryString());
        System.out.println(eval.toClassDetailsString());
        System.out.println(eval.toMatrixString());
    }
    
    /**
     * 分类结果内部类
     */
    public static class ClassificationResult {
        private String className;
        private double confidence;
        private double[] distribution;
        
        public ClassificationResult(String className, double confidence, double[] distribution) {
            this.className = className;
            this.confidence = confidence;
            this.distribution = distribution;
        }
        
        public String getClassName() {
            return className;
        }
        
        public double getConfidence() {
            return confidence;
        }
        
        public double[] getDistribution() {
            return distribution;
        }
        
        @Override
        public String toString() {
            return String.format("类别: %s, 置信度: %.2f", className, confidence);
        }
    }
    
    /**
     * 主函数 - 用于测试和命令行调用
     */
    public static void main(String[] args) {
        try {
            if (args.length < 2) {
                System.out.println("用法: java ExerciseClassifier <train|classify> <data_path> [model_path]");
                return;
            }
            
            ExerciseClassifier classifier = new ExerciseClassifier();
            String mode = args[0];
            
            if (mode.equals("train")) {
                String dataPath = args[1];
                String modelPath = args.length > 2 ? args[2] : "models/exercise_classifier.model";
                classifier.trainModel(dataPath, "J48");
                classifier.saveModel(modelPath);
                
                // 如果有测试数据，进行评估
                if (args.length > 3) {
                    classifier.evaluateModel(args[3]);
                }
            } else if (mode.equals("classify")) {
                String modelPath = args[1];
                classifier.loadModel(modelPath);
                
                // 这里应该从args[2]读取特征，简化示例
                System.out.println("分类模式已加载，等待输入特征...");
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

