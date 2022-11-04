# Cancer_Finder

## Installation

```
pip install -r requirements.txt
```

## Start app

```
python app.py
```

## View results

```

```

## Documentation
### Intro
- The app consists of two parts, back (Cancer_Finder repo) and front(Cancer_Finder_F repo)
- Back provides functionality:
  - neural network, which can generate defects on healthy CT image
  - contains dcm images original CT
  - contains dcm images segmentation
  - provide access to CT images from front and get new segmentation from front

- Front provides functionality:
  - Get CT image and show as image in redactor
  - Segmentation redactor and save it to server

### Back
- 