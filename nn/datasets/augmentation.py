import albumentations as albu
import cv2


def aug_transforms():
    return [
        albu.VerticalFlip(),
        albu.HorizontalFlip(),
        albu.Rotate(limit=180, interpolation=cv2.INTER_LANCZOS4, border_mode=cv2.BORDER_WRAP, always_apply=False,
                    p=0.6),
        albu.ElasticTransform(alpha=10, sigma=50, alpha_affine=28,
                              interpolation=cv2.INTER_LANCZOS4, border_mode=cv2.BORDER_WRAP,
                              always_apply=False, approximate=False, p=0.6),
        albu.GridDistortion(num_steps=20, distort_limit=0.2, interpolation=cv2.INTER_LANCZOS4,
                            border_mode=cv2.BORDER_WRAP,
                            always_apply=False, p=0.5)
    ]


transforms = albu.Compose(aug_transforms())


def augment_image(image):
    return transforms(image=image)["image"]
