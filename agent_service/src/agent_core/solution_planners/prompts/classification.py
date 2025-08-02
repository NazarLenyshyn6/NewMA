"""..."""

from langchain.prompts import ChatPromptTemplate

from agent_core.subtask_selectors.enums.classification import ClassificationSubTask
from agent_core.solution_planners.prompts.base import BaseSolutionPlaningPromptBuilder

CLASSIFICATION_REFLECTION_PROMPTS: dict[ClassificationSubTask, ChatPromptTemplate] = {
    ClassificationSubTask.CATEGORICAL_ENCODING: BaseSolutionPlaningPromptBuilder(
        "You are a categorical encoding specialist. Reflect deeply on which categorical features have already been encoded, "
        "the methods applied, and any known issues or gaps. Your goal is to continue precisely from the last completed step, "
        "identifying the next categorical variable or encoding technique that needs to be applied or improved without repeating past work."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.FEATURE_SCALING: BaseSolutionPlaningPromptBuilder(
        "You are a feature scaling expert. Carefully review which numerical features have been scaled, the scaling methods used, "
        "and any scaling inconsistencies or remaining features to handle. Continue from the last completed step to plan and execute "
        "the next appropriate scaling action, ensuring no redundant transformations."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.FEATURE_SELECTION: BaseSolutionPlaningPromptBuilder(
        "You are a feature selection strategist. Analyze which features have already been evaluated or removed based on importance or correlation, "
        "and which selection methods have been applied. From this reflective state, decide on the next set of features to assess or prune, "
        "continuing smoothly without duplication."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.DATA_SPLITTING: BaseSolutionPlaningPromptBuilder(
        "You are responsible for dataset partitioning. Reflect on the train/validation/test splits already made, including stratification or random sampling choices. "
        "Confirm what remains to ensure robust evaluation splits, and carefully plan the next splitting or resampling step from where the previous step concluded."
    ).build_solution_planing_prompt(),
    # === Model Training and Hyperparameter Tuning ===
    ClassificationSubTask.MODEL_SELECTION: BaseSolutionPlaningPromptBuilder(
        "You are a model selection advisor. Reflect deeply on models already considered or tested, their relative strengths and weaknesses on this dataset, "
        "and any architectural decisions or assumptions. Thoughtfully plan the next model(s) to evaluate, advancing without repeating prior trials."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.TRAINING: BaseSolutionPlaningPromptBuilder(
        "You are a training orchestrator. Carefully review which models have been trained, the data subsets used, training configurations, and results. "
        "From this reflective position, select the next training runs or configurations to perform, building incrementally and avoiding re-training identical setups."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.HYPERPARAMETER_TUNING: BaseSolutionPlaningPromptBuilder(
        "You are a hyperparameter tuning specialist. Review which search strategies, parameter ranges, and combinations have been explored so far, "
        "along with outcomes. Thoughtfully decide the next promising hyperparameter regions or techniques to explore, continuing precisely from prior progress."
    ).build_solution_planing_prompt(),
    # === Model Evaluation and Validation ===
    ClassificationSubTask.MODEL_EVALUATION: BaseSolutionPlaningPromptBuilder(
        "You are a model evaluator. Reflect on which evaluation datasets, metrics, and validation methods have been applied to each candidate model. "
        "From this clear understanding, plan the next evaluations or analyses to gain deeper insight into model performance without redundancy."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.CROSS_VALIDATION: BaseSolutionPlaningPromptBuilder(
        "You are a cross-validation expert. Consider folds, repetitions, and stratifications already completed, and their results. "
        "Design the next cross-validation experiments or refinements to more robustly estimate performance, continuing systematically from previous work."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.PERFORMANCE_METRICS: BaseSolutionPlaningPromptBuilder(
        "You are a performance metrics analyst. Reflect on metrics like accuracy, precision, recall, F1, and ROC-AUC already calculated and interpreted. "
        "Identify the next relevant metric or threshold analysis to deepen understanding of model behavior without repeating calculations."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.CONFUSION_MATRIX: BaseSolutionPlaningPromptBuilder(
        "You are a confusion matrix analyst. Review confusion matrices generated at different thresholds or for different models, "
        "and reflect on error patterns discovered. Plan the next diagnostic or visualization step to clarify model weaknesses or strengths."
    ).build_solution_planing_prompt(),
    # === Model Interpretation and Deployment ===
    ClassificationSubTask.FEATURE_IMPORTANCE: BaseSolutionPlaningPromptBuilder(
        "You are a feature importance investigator. Carefully consider which importance measures or explainability methods (e.g., SHAP, permutation) have been applied. "
        "Plan the next interpretability analysis step to enhance understanding of model decisions, continuing logically from previous insights."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.MODEL_EXPLANATION: BaseSolutionPlaningPromptBuilder(
        "You are a model explanation specialist. Reflect on explanation techniques already applied and documented, their findings, and limitations. "
        "Determine the next explanation approach or visualization to pursue, building on prior explanations without redundancy."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.MODEL_SERIALIZATION: BaseSolutionPlaningPromptBuilder(
        "You are responsible for model serialization and persistence. Reflect on models saved, versioned, or deployed so far. "
        "Plan the next saving, packaging, or deployment readiness actions required to ensure model reproducibility and maintainability."
    ).build_solution_planing_prompt(),
    ClassificationSubTask.MONITORING: BaseSolutionPlaningPromptBuilder(
        "You are a model monitoring engineer. Reflect on metrics and data drift monitoring currently in place or planned. "
        "From this assessment, design the next steps for performance tracking, alerting, or retraining triggers to keep the model reliable post-deployment."
    ).build_solution_planing_prompt(),
}
