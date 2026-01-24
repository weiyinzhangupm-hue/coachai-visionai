package com.virtualtrainer;

import weka.core.Instances;
import weka.core.Instance;
import weka.core.Attribute;
import weka.classifiers.Evaluation;
import weka.classifiers.Classifier;
import weka.attributeSelection.AttributeSelection;
import weka.attributeSelection.GeneticSearch;
import weka.attributeSelection.CfsSubsetEval;

import java.util.Random;
import java.util.ArrayList;

/**
 * 遗传算法特征选择器
 * 使用遗传算法优化特征子集
 */
public class GeneticFeatureSelector {
    
    private int populationSize;
    private int numGenerations;
    private double mutationRate;
    private double crossoverRate;
    private Random random;
    
    /**
     * 构造函数
     * 
     * @param populationSize 种群大小
     * @param numGenerations 代数
     * @param mutationRate 变异率
     * @param crossoverRate 交叉率
     */
    public GeneticFeatureSelector(int populationSize, int numGenerations, 
                                   double mutationRate, double crossoverRate) {
        this.populationSize = populationSize;
        this.numGenerations = numGenerations;
        this.mutationRate = mutationRate;
        this.crossoverRate = crossoverRate;
        this.random = new Random();
    }
    
    /**
     * 使用Weka内置的遗传搜索进行特征选择
     * 
     * @param data 训练数据
     * @return 选中的特征索引数组
     * @throws Exception 如果选择失败
     */
    public int[] selectFeaturesWithWeka(Instances data) throws Exception {
        System.out.println("开始使用Weka遗传算法进行特征选择...");
        
        // 创建特征选择器
        AttributeSelection selector = new AttributeSelection();
        
        // 使用遗传搜索
        GeneticSearch search = new GeneticSearch();
        search.setPopulationSize(populationSize);
        search.setMaxGenerations(numGenerations);
        search.setCrossoverProb(crossoverRate);
        search.setMutationProb(mutationRate);
        
        // 使用相关性特征子集评估器
        CfsSubsetEval eval = new CfsSubsetEval();
        
        selector.setEvaluator(eval);
        selector.setSearch(search);
        
        // 执行特征选择
        selector.SelectAttributes(data);
        
        // 获取选中的特征
        int[] selectedAttributes = selector.selectedAttributes();
        
        System.out.println("特征选择完成:");
        System.out.println("原始特征数: " + (data.numAttributes() - 1));
        System.out.println("选中特征数: " + selectedAttributes.length);
        System.out.print("选中的特征索引: ");
        for (int attr : selectedAttributes) {
            System.out.print(attr + " ");
        }
        System.out.println();
        
        return selectedAttributes;
    }
    
    /**
     * 自定义遗传算法实现（用于教学和演示）
     * 
     * @param data 训练数据
     * @param classifier 用于评估的分类器
     * @return 最优特征子集
     * @throws Exception 如果执行失败
     */
    public boolean[] selectFeaturesCustom(Instances data, Classifier classifier) throws Exception {
        int numFeatures = data.numAttributes() - 1; // 排除类别属性
        
        // 初始化种群
        boolean[][] population = initializePopulation(numFeatures);
        double[] fitness = new double[populationSize];
        
        // 最优个体
        boolean[] bestIndividual = null;
        double bestFitness = Double.NEGATIVE_INFINITY;
        
        // 进化循环
        for (int generation = 0; generation < numGenerations; generation++) {
            // 评估适应度
            for (int i = 0; i < populationSize; i++) {
                fitness[i] = evaluateFitness(population[i], data, classifier);
                
                // 更新最优解
                if (fitness[i] > bestFitness) {
                    bestFitness = fitness[i];
                    bestIndividual = population[i].clone();
                }
            }
            
            if (generation % 10 == 0) {
                System.out.printf("代数 %d: 最优适应度 = %.4f%n", generation, bestFitness);
            }
            
            // 创建新种群
            boolean[][] newPopulation = new boolean[populationSize][numFeatures];
            
            for (int i = 0; i < populationSize; i++) {
                // 选择
                boolean[] parent1 = tournamentSelection(population, fitness);
                boolean[] parent2 = tournamentSelection(population, fitness);
                
                // 交叉
                boolean[] offspring;
                if (random.nextDouble() < crossoverRate) {
                    offspring = crossover(parent1, parent2);
                } else {
                    offspring = parent1.clone();
                }
                
                // 变异
                mutate(offspring);
                
                newPopulation[i] = offspring;
            }
            
            // 精英保留：保留最优个体
            newPopulation[0] = bestIndividual.clone();
            
            population = newPopulation;
        }
        
        System.out.println("遗传算法优化完成");
        System.out.printf("最优适应度: %.4f%n", bestFitness);
        System.out.printf("选中特征数: %d / %d%n", countSelected(bestIndividual), numFeatures);
        
        return bestIndividual;
    }
    
    /**
     * 初始化种群
     */
    private boolean[][] initializePopulation(int numFeatures) {
        boolean[][] population = new boolean[populationSize][numFeatures];
        
        for (int i = 0; i < populationSize; i++) {
            for (int j = 0; j < numFeatures; j++) {
                population[i][j] = random.nextDouble() < 0.5;
            }
        }
        
        return population;
    }
    
    /**
     * 评估适应度
     * 适应度 = 分类准确率 - α * (特征数 / 总特征数)
     */
    private double evaluateFitness(boolean[] individual, Instances data, Classifier classifier) throws Exception {
        // 如果没有选中任何特征，返回最低适应度
        if (countSelected(individual) == 0) {
            return 0.0;
        }
        
        // 创建特征子集数据
        Instances subset = filterInstances(data, individual);
        
        // 交叉验证评估
        Evaluation eval = new Evaluation(subset);
        eval.crossValidateModel(classifier, subset, 5, new Random(1));
        
        double accuracy = eval.pctCorrect() / 100.0;
        double featureRatio = (double) countSelected(individual) / individual.length;
        double alpha = 0.1; // 特征数量惩罚系数
        
        return accuracy - alpha * featureRatio;
    }
    
    /**
     * 锦标赛选择
     */
    private boolean[] tournamentSelection(boolean[][] population, double[] fitness) {
        int tournamentSize = 3;
        int bestIdx = random.nextInt(populationSize);
        double bestFitness = fitness[bestIdx];
        
        for (int i = 1; i < tournamentSize; i++) {
            int idx = random.nextInt(populationSize);
            if (fitness[idx] > bestFitness) {
                bestIdx = idx;
                bestFitness = fitness[idx];
            }
        }
        
        return population[bestIdx].clone();
    }
    
    /**
     * 单点交叉
     */
    private boolean[] crossover(boolean[] parent1, boolean[] parent2) {
        int length = parent1.length;
        boolean[] offspring = new boolean[length];
        int crossoverPoint = random.nextInt(length);
        
        for (int i = 0; i < length; i++) {
            offspring[i] = i < crossoverPoint ? parent1[i] : parent2[i];
        }
        
        return offspring;
    }
    
    /**
     * 变异
     */
    private void mutate(boolean[] individual) {
        for (int i = 0; i < individual.length; i++) {
            if (random.nextDouble() < mutationRate) {
                individual[i] = !individual[i];
            }
        }
    }
    
    /**
     * 统计选中的特征数
     */
    private int countSelected(boolean[] individual) {
        int count = 0;
        for (boolean selected : individual) {
            if (selected) count++;
        }
        return count;
    }
    
    /**
     * 根据特征选择过滤数据
     */
    private Instances filterInstances(Instances data, boolean[] selected) throws Exception {
        // 创建新的属性列表
        ArrayList<Attribute> attributes = new ArrayList<>();
        
        for (int i = 0; i < selected.length; i++) {
            if (selected[i]) {
                attributes.add((Attribute) data.attribute(i).copy());
            }
        }
        
        // 添加类别属性
        attributes.add((Attribute) data.classAttribute().copy());
        
        // 创建新数据集
        Instances filtered = new Instances("filtered", attributes, data.numInstances());
        filtered.setClassIndex(filtered.numAttributes() - 1);
        
        // 复制实例
        for (int i = 0; i < data.numInstances(); i++) {
            Instance oldInst = data.instance(i);
            double[] values = new double[filtered.numAttributes()];
            int newIdx = 0;
            
            for (int j = 0; j < selected.length; j++) {
                if (selected[j]) {
                    values[newIdx++] = oldInst.value(j);
                }
            }
            values[newIdx] = oldInst.classValue();
            
            filtered.add(new weka.core.DenseInstance(1.0, values));
        }
        
        return filtered;
    }
    
    /**
     * 主函数 - 测试用
     */
    public static void main(String[] args) {
        try {
            System.out.println("遗传算法特征选择器测试");
            System.out.println("使用方式: java GeneticFeatureSelector <data_path>");
            
            // 示例配置
            int popSize = 50;
            int generations = 100;
            double mutationRate = 0.01;
            double crossoverRate = 0.8;
            
            System.out.println("配置:");
            System.out.println("- 种群大小: " + popSize);
            System.out.println("- 代数: " + generations);
            System.out.println("- 变异率: " + mutationRate);
            System.out.println("- 交叉率: " + crossoverRate);
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

