import pandas as pd
import numpy as np
import re

persian_to_english = {
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
}

def load_data(path="Data/divar_final.csv"):
    df = pd.read_csv(path)
    return df

def drop_col(df):
    drop_cols = [col for col in ["token", "title", "desc", "brand_model"] if col in df.columns]
    df = df.drop(columns=drop_cols)
    return df

def clean_price(text):
    if pd.isna(text):
        return None

    for fa, en in persian_to_english.items():
        text = text.replace(fa, en)
        
    text = re.sub(r'[^\d]', '', text)
    if text == '':
        return None
    
    return int(text)




def to_english_digits(text):
    text = str(text)
    for fa, en in persian_to_english.items():
        text = text.replace(fa, en)
    return text

def split_year(text):
    if pd.isna(text):
        return pd.Series([None, None])
    
    text = to_english_digits(text)
    numbers = re.findall(r'\d+', text)
    
    if len(numbers) == 2:
        shamsi, miladi = numbers
        return pd.Series([int(shamsi), int(miladi)])
    elif len(numbers) == 1:
        num = int(numbers[0])
        if num < 1500:  
            return pd.Series([num, None])  
        else:
            return pd.Series([None, num])  
    else:
        return pd.Series([None, None])

def color_transition(df):
    color_translation = {
    'آبی': 'Blue',
    'سفید': 'White',
    'نقره‌ای': 'Silver',
    'زرد': 'Yellow',
    'طوسی': 'Gray',
    'عنابی': 'Maroon',
    'مشکی': 'Black',
    'خاکستری': 'Gray',
    'سفید صدفی': 'Pearl White',
    'قرمز': 'Red',
    'سایر': 'Other',
    'بژ': 'Beige',
    'ذغالی': 'Charcoal',
    'یشمی': 'Jade',
    'نوک‌مدادی': 'Pencil Gray',
    'دلفینی': 'Dolphin Gray',
    'سرمه‌ای': 'Navy Blue',
    'تیتانیوم': 'Titanium',
    'قهوه‌ای': 'Brown',
    'نقرآبی': 'Silver Blue',
    'آلبالویی': 'Cherry',
    'سبز': 'Green',
    'برنز': 'Bronze',
    'طلایی': 'Gold',
    'نارنجی': 'Orange',
    'سربی': 'Lead Gray',
    'کربن‌بلک': 'Carbon Black',
    'اطلسی': 'Atlas',
    'زرشکی': 'Crimson',
    'کرم': 'Cream',
    'زیتونی': 'Olive',
    'بادمجانی': 'Eggplant',
    'بنفش': 'Purple',
    'مسی': 'Copper',
    'گیلاسی': 'Cherry Red',
    'خاکی': 'Khaki',
    'عدسی': 'Lentil Brown',
}

    df['color'] = df['color'].map(color_translation)
    return df

def gearbox_transition(df):
    gearbox_translation = {
        'دنده‌ای': 'Manual',
        'اتوماتیک': 'Automatic',
    }

    df['gearbox'] = df['gearbox'].map(gearbox_translation)
    return df

def fuel_transition(df):
    fuel_translation = {
        'بنزین': 'Gasoline',
        'دوگانه‌سوز شرکتی': 'Bi-fuel (Factory)',
        'دوگانه‌سوز دستی': 'Bi-fuel (Aftermarket)',
        'هیبرید': 'Hybrid',
        'برق': 'Electric',
        'پلاگین هیبرید': 'Plug-in Hybrid',
        'گازوئیل': 'Diesel',
    }

    df['fuel'] = df['fuel'].map(fuel_translation)
    return df

def score_engine_transition(df):
    score_engine_translation = {
        'سالم': 'Healthy',
        'تعیین‌نشده': np.nan,
        'نیاز به تعمیر': 'Needs Repair',
        'تعویض شده': 'Replaced',
    }

    df['score_engine'] = df['score_engine'].map(score_engine_translation)
    return df

def score_chassis_transition(df):
    score_chassis_translation = {
        'سالم و پلمپ': 'Healthy & Sealed',
        'تعیین‌نشده': np.nan,
        'ضربه‌خورده': 'Damaged',
        'رنگ‌شده': 'Repainted',
    }

    df['score_chassis'] = df['score_chassis'].map(score_chassis_translation)
    return df

def score_body_transition(df):
    score_body_translation = {
        'سالم و بی‌خط و خش': 'Healthy, No Scratches',
        'خط و خش جزیی': 'Minor Scratches',
        'دوررنگ': 'Two-tone (Repainted)',
        'صافکاری بی‌رنگ': 'Bodywork, No Paint',
        'تمام‌رنگ': 'Fully Repainted',
        'تصادفی': 'Accidented',
        'اوراقی': 'Scrapped',
    }

    persian_to_english_map = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
    }

    def translate_and_extract(text):
        if pd.isna(text):
            return pd.Series([None, None])
        
        text = str(text)
        
        if 'رنگ‌شدگی در' in text:
            num_text = text
            for fa, en in persian_to_english_map.items():
                num_text = num_text.replace(fa, en)
            match = re.search(r'\d+', num_text)
            region_count = int(match.group()) if match else None
            return pd.Series([f'Repainted in {region_count} area(s)', region_count])
        
        translated = score_body_translation.get(text, None)
        return pd.Series([translated, 0])  

    df[['score_body', 'score_body_region_count']] = df['score_body'].apply(translate_and_extract)
    return df

def score_gearbox_transition(df):
    score_gearbox_translation = {
        'سالم و پلمپ': 'Healthy & Sealed',
        'تعمیر شده': 'Repaired',
        'نیاز به تعمیر جزئی': 'Needs Minor Repair',
        'نیاز به تعمیر اساسی': 'Needs Major Repair',
    }

    df['score_gearbox'] = df['score_gearbox'].map(score_gearbox_translation)
    return df
    
def detect_mixed_types(df):
    mixed_types = {}
    for column in df.columns:
        types = df[column].apply(lambda v: type(v).__name__).value_counts()
        if len(types) > 1:
            mixed_types[column] = types.to_dict()
    return mixed_types


def handle_missing(df, threshold=3):
    missing_percent = (df.isna().sum() / len(df)) * 100
    for col in df.columns:
        if missing_percent[col] == 0:
            continue
        elif missing_percent[col] < threshold:
            df = df.dropna(subset=[col])
        else:
            if df[col].dtype in ['object', 'str']:
                df[col] = df[col].fillna(df[col].mode()[0])
            else:
                df[col] = df[col].fillna(df[col].median())
    return df

def detect_outliers(df):
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        count = mask.sum()
        percent = (count / len(df)) * 100

        print(f"{col:<20} ---> {count:>5} outliers ({percent:.2f}%)")
        print(f"bounds: [{lower_bound:,.2f} , {upper_bound:,.2f}]")

        if count > 0:
            outlier_values = df.loc[mask, col].sort_values()
            print(f"lowest: {outlier_values.head(10).tolist()}")
            print(f"highest: {outlier_values.tail(10).tolist()}")
        print()

# def impute_outliers(df, cols):

#     for col in cols:
#         Q1 = df[col].quantile(0.25)
#         Q3 = df[col].quantile(0.75)
#         IQR = Q3 - Q1

#         lower_bound = Q1 - 1.5 * IQR
#         upper_bound = Q3 + 1.5 * IQR

#         median_val = df[col].median()

#         mask = (df[col] < lower_bound) | (df[col] > upper_bound)

#         print(f"{col} ---> {mask.sum()} outliers imputed")

#         df.loc[mask, col] = median_val

