# Помоги роботу навести порядок

## Как запустить?

Установите зависимости:
```sh
pip install Pillow
```

Измените пути на нужные файлы в функции *image_augmentation*:
```sh
if __name__== '__main__':
    image_augmentation("train_dataset/train_images", "train_dataset/new_images")
```

Измените пути на нужные файлы в функции *dataset_adder*:
```sh
def main():
    test = DatasetAdder()  
    test.dataset_adder('train_dataset\\train_dataset.json')
    
if __name__=='__main__':
    main()
```
