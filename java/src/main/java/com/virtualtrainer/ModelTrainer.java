package com.virtualtrainer;

import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.core.converters.CSVLoader;
import weka.core.converters.ArffSaver;
import weka.classifiers.Classifier;
import weka.classifiers.trees.J48;

import java.io.File;

/**
 * 模型训练器
 * 用于训练和评估分类模型
 */
public class ModelTrainer {
    
    /**
     * 训练完整流程
     * 
     * @param trainDataPath 训练数据路径
     * @param testDataPath 测试数据路径（可选）
     * @param modelOutputPath 模型保存路径
     * @param useGA 是否使用遗传算法进行特征选择
     * @throws Exception 如果训练失败
     */
    public static void trainFullPipeline(String trainDataPath, String testDataPath,
                                        String modelOutputPath, boolean useGA) throws Exception {
        System.out.println("=== 虚拟健身教练 - 模型训练流程 ===");
        System.out.println();
        
        // 1. 加载数据
        System.out.println("1. 加载训练数据...");
        Instances trainData = loadData(trainDataPath);
        System.out.println("   训练实例数: " + trainData.numInstances());
        System.out.println("   特征数: " + (trainData.numAttributes() - 1));
        System.out.println("   类别数: " + trainData.numClasses());
        System.out.println();
        
        // 2. 特征选择（可选）
        int[] selectedFeatures = null;
        if (useGA) {
            System.out.println("2. 使用遗传算法进行特征选择...");
            GeneticFeatureSelector gaSelector = new GeneticFeatureSelector(
                50,    // 种群大小
                100,   // 代数
                0.01,  // 变异率
                0.8    // 交叉率
            );
            selectedFeatures = gaSelector.selectFeaturesWithWeka(trainData);
            System.out.println("   选中特征数: " + selectedFeatures.length);
            System.out.println();
            
            // 根据选中特征过滤数据
            trainData = filterByFeatures(trainData, selectedFeatures);
        } else {
            System.out.println("2. 跳过特征选择，使用所有特征");
            System.out.println();
        }
        
        // 3. 训练模型
        System.out.println("3. 训练分类器 (J48决策树)...");
        ExerciseClassifier classifier = new ExerciseClassifier();
        classifier.trainModel(convertToTempFile(trainData), "J48");
        System.out.println("   训练完成");
        System.out.println();
        
        // 4. 评估模型
        if (testDataPath != null && !testDataPath.isEmpty()) {
            System.out.println("4. 评估模型性能...");
            Instances testData = loadData(testDataPath);
            if (selectedFeatures != null) {
                testData = filterByFeatures(testData, selectedFeatures);
            }
            classifier.evaluateModel(convertToTempFile(testData));
            System.out.println();
        }
        
        // 5. 保存模型
        System.out.println("5. 保存训练好的模型...");
        classifier.saveModel(modelOutputPath);
        System.out.println();
        
        System.out.println("=== 训练流程完成 ===");
    }
    
    /**
     * 加载数据（支持CSV和ARFF格式）
     */
    private static Instances loadData(String dataPath) throws Exception {
        DataSource source = new DataSource(dataPath);
        Instances data = source.getDataSet();
        
        // 设置类别属性（假设是最后一列）
        if (data.classIndex() == -1) {
            data.setClassIndex(data.numAttributes() - 1);
        }
        
        return data;
    }
    
    /**
     * 根据特征索引过滤数据
     */
    private static Instances filterByFeatures(Instances data, int[] selectedFeatures) throws Exception {
        weka.filters.unsupervised.attribute.Remove remove = new weka.filters.unsupervised.attribute.Remove();
        
        // 构建要保留的属性索引字符串
        StringBuilder indices = new StringBuilder();
        for (int i = 0; i < selectedFeatures.length; i++) {
            indices.append(selectedFeatures[i] + 1); // Weka索引从1开始
            if (i < selectedFeatures.length - 1) {
                indices.append(",");
            }
        }
        indices.append(",last"); // 保留类别属性
        
        remove.setAttributeIndices(indices.toString());
        remove.setInvertSelection(false);
        remove.setInputFormat(data);
        
        return weka.filters.Filter.useFilter(data, remove);
    }
    
    /**
     * 将Instances转换为临时ARFF文件（辅助方法）
     */
    private static String convertToTempFile(Instances data) throws Exception {
        String tempPath = "temp_data_" + System.currentTimeMillis() + ".arff";
        ArffSaver saver = new ArffSaver();
        saver.setInstances(data);
        saver.setFile(new File(tempPath));
        saver.writeBatch();
        return tempPath;
    }
    
    /**
     * CSV转ARFF格式
     */
    public static void convertCSVtoARFF(String csvPath, String arffPath) throws Exception {
        CSVLoader loader = new CSVLoader();
        loader.setSource(new File(csvPath));
        Instances data = loader.getDataSet();
        
        // 保存为ARFF
        ArffSaver saver = new ArffSaver();
        saver.setInstances(data);
        saver.setFile(new File(arffPath));
        saver.writeBatch();
        
        System.out.println("转换完成: " + csvPath + " -> " + arffPath);
    }
    
    /**
     * 主函数 - 命令行工具
     */
    public static void main(String[] args) {
        try {
            if (args.length < 2) {
                System.out.println("用法:");
                System.out.println("  训练: java ModelTrainer train <train_data> <model_output> [test_data] [use_ga]");
                System.out.println("  转换: java ModelTrainer convert <csv_file> <arff_file>");
                System.out.println();
                System.out.println("参数:");
                System.out.println("  train_data   - 训练数据文件（CSV或ARFF）");
                System.out.println("  model_output - 模型输出路径");
                System.out.println("  test_data    - 测试数据文件（可选）");
                System.out.println("  use_ga       - 是否使用遗传算法（true/false，默认false）");
                return;
            }
            
            String mode = args[0];
            
            if (mode.equals("train")) {
                String trainData = args[1];
                String modelOutput = args[2];
                String testData = args.length > 3 ? args[3] : null;
                boolean useGA = args.length > 4 ? Boolean.parseBoolean(args[4]) : false;
                
                trainFullPipeline(trainData, testData, modelOutput, useGA);
                
            } else if (mode.equals("convert")) {
                String csvFile = args[1];
                String arffFile = args[2];
                convertCSVtoARFF(csvFile, arffFile);
            } else {
                System.out.println("未知模式: " + mode);
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

