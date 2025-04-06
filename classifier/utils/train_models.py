import os
import pandas as pd
from transformers import TrainingArguments
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset
from sklearn.metrics import roc_curve
import tensorflow as tf

# چک کردن اینکه TensorFlow آیا از GPU استفاده می‌کند یا نه
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# بارگیری داده‌ها
dataset = load_dataset('saattrupdan/womens-clothing-ecommerce-reviews')
train_dataset = dataset["train"]
val_dataset = dataset["val"]
test_dataset = dataset["test"]

# توکنایزر کردن داده‌ها
def tokenize_function(examples, tokenizer):
    return tokenizer(examples["review_text"], padding="max_length", truncation=True)

def train_and_evaluate(model_name, train_dataset, val_dataset, test_dataset):
    # بارگیری مدل و توکنایزر
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model_dir = f"./saved_model_{model_name}"
    
    # اگر مدل ذخیره شده است، از آن استفاده کن
    if os.path.exists(model_dir):
        model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        print(f"Model loaded from {model_dir}")
    else:
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)  # برای دو کلاس: توصیه شده یا نه
    
        # توکنایز کردن داده‌ها
        train_dataset = train_dataset.map(lambda examples: tokenize_function(examples, tokenizer), batched=True)
        val_dataset = val_dataset.map(lambda examples: tokenize_function(examples, tokenizer), batched=True)
        test_dataset = test_dataset.map(lambda examples: tokenize_function(examples, tokenizer), batched=True)

        train_dataset = train_dataset.rename_column("recommended_ind", "labels")
        val_dataset = val_dataset.rename_column("recommended_ind", "labels")
        test_dataset = test_dataset.rename_column("recommended_ind", "labels")
        # ایجاد پوشه‌ها اگر وجود ندارند
        # ایجاد پوشه‌ها اگر وجود ندارند
        os.makedirs('./results', exist_ok=True)  # برای ذخیره نتایج
        os.makedirs('./results/logs', exist_ok=True)  # برای ذخیره لاگ‌های TensorBoard
        os.makedirs('./saved_models', exist_ok=True)  # برای ذخیره مدل‌ها
                # تنظیمات آموزش
        training_args = TrainingArguments(
        output_dir='./results',
        overwrite_output_dir=True,
        do_train=True,
        do_eval=True,
        evaluation_strategy='epoch',
        logging_dir='./results/logs',
        logging_strategy='epoch',
        logging_steps=500,
        report_to=['tensorboard'],
        save_steps=500,
        save_strategy='epoch',
        save_total_limit=3,
        load_best_model_at_end=True,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        learning_rate=2e-05,
        seed=42,
        optim='adamw_torch'
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            tokenizer=tokenizer
        )

        # شروع آموزش
        trainer.train()

        # ذخیره مدل و توکنایزر
        model.save_pretrained(model_dir)
        tokenizer.save_pretrained(model_dir)

    # پیش‌بینی‌های مدل
    predictions = trainer.predict(test_dataset)
    pred_probs = predictions.predictions  # احتمال پیش‌بینی‌شده برای دسته‌های مختلف
    pred_labels = pred_probs.argmax(axis=-1)  # انتخاب کلاس با بالاترین احتمال

    # مقایسه با برچسب‌های واقعی
    true_labels = test_dataset["labels"]

    # محاسبه متریک‌ها
    accuracy = accuracy_score(true_labels, pred_labels)
    precision = precision_score(true_labels, pred_labels, average='binary')
    recall = recall_score(true_labels, pred_labels, average='binary')
    f1 = f1_score(true_labels, pred_labels, average='binary')
    
    # محاسبه AUC-ROC
    auc_roc = roc_auc_score(true_labels, pred_probs[:, 1])  # احتمال پیش‌بینی‌شده برای کلاس مثبت

    # ذخیره متریک‌ها در یک فایل
    metrics_file = f'./results/{model_name}_metrics.txt'
    with open(metrics_file, 'w') as f:
        f.write(f"Model: {model_name}\n")
        f.write(f"Accuracy: {accuracy}\n")
        f.write(f"Precision: {precision}\n")
        f.write(f"Recall: {recall}\n")
        f.write(f"F1-Score: {f1}\n")
        f.write(f"AUC-ROC: {auc_roc}\n")

    # رسم نمودار ROC و ذخیره آن
    fpr, tpr, _ = roc_curve(true_labels, pred_probs[:, 1])  # محاسبه منحنی ROC
    plt.figure()
    plt.plot(fpr, tpr, color='blue', label=f'AUC = {auc_roc:.2f}')
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {model_name}')
    plt.legend(loc='lower right')
    roc_curve_file = f'./results/{model_name}_roc_curve.png'
    plt.savefig(roc_curve_file)
    plt.close()

    # محاسبه و رسم ماتریس اشتباهات و ذخیره آن
    cm = confusion_matrix(true_labels, pred_labels)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Negative", "Positive"], yticklabels=["Negative", "Positive"])
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title(f'Confusion Matrix - {model_name}')
    confusion_matrix_file = f'./results/{model_name}_confusion_matrix.png'
    plt.savefig(confusion_matrix_file)
    plt.close()

    # چاپ متریک‌ها
    print(f"Model: {model_name}")
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-Score: {f1}")
    print(f"AUC-ROC: {auc_roc}")

# آموزش و ارزیابی مدل‌های مختلف
models = [
    "bert-base-uncased",
    "distilbert-base-uncased",
]

for model_name in models:
    train_and_evaluate(model_name, train_dataset, val_dataset, test_dataset)