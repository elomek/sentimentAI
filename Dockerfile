# استفاده از تصویر پایه پایتون 3.10 و CUDA مناسب برای TensorFlow و PyTorch
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# نصب پکیج‌های سیستم‌عامل برای TensorFlow و PyTorch
RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# لینک کردن python به python3.10
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# لینک کردن pip3 به pip
RUN rm -f /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip

# ارتقاء pip
RUN pip3 install --upgrade pip

# تنظیم محیط پایتون
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# پوشه کاری پروژه
WORKDIR /code 

# کپی کردن کدها به کانتینر
COPY . /code/

# نصب پکیج‌های مورد نیاز از requirements.txt
RUN pip install -r requirements.txt --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

# نصب TensorFlow GPU (و یا هر پکیج دیگری مانند PyTorch در صورت نیاز)
RUN pip install tensorflow-gpu --timeout=300


# دستور اجرای برنامه
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "classifier/utils/train_models.py"]

