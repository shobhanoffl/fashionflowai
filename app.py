from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import csv
import time
import datetime

import requests
from bs4 import BeautifulSoup

import torch
from transformers import AutoTokenizer
import transformers
from IPython.display import YouTubeVideo

from stablediffusion import stablediffusion

app = Flask(__name__)
app.secret_key = 'your_secret_key'  


# def saveLogs():



# Load product data from CSV
def load_products():
    products = []
    with open('products.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append(row)
    return products

@app.route('/fashion')
def index():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    products = load_products()
    return render_template('index.html', user_email=session['user_email'], products=products)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['user_email'] = request.form['user_email']
#         return redirect(url_for('index'))
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['user_email']
        user_password = request.form['passw']

        # Load user data from CSV
        user_data = []
        with open('user_data.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_data.append(row)
        for user in user_data:
            print(user['email'],user_email,user['password'],user_password)
            if user['email'] == user_email and user['password'] == user_password:
                session['user_email'] = user['name']
                return redirect(url_for('index'))

        # If login fails
        return render_template('login.html')

    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        gender = request.form['gender']
        age = request.form['age']
        skin_tone = request.form['skin-tone']
        region = request.form['region']
        body_shape = request.form['bodyshape']

        # Write the data to a CSV file
        with open('user_other_data.csv', 'a', newline='') as csvfile:
            fieldnames = ['Gender', 'Age', 'Skin Tone', 'Country/Region', 'Body Shape']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({'Gender': gender, 'Age': age, 'Skin Tone': skin_tone,
                             'Country/Region': region, 'Body Shape': body_shape})

        return redirect(url_for('index'))

@app.route('/cart')
def cart():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    products = load_products()
    cart_products = [product for product in cart if product in products]

    total_price = sum(float(product['price']) for product in cart_products)

    return render_template('cart.html', user_email=session['user_email'], cart_products=cart_products, total_price=total_price)

@app.route('/buy')
def buy():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('buy.html')

@app.route('/doc')
def doc():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('doc.html')

@app.route('/profile')
def profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    # You can retrieve additional user details if needed
    user_details = {
        'username': session['user_email'],
        'email': 'rshobhan02@gmail.com',
        'address': 'Thindal, Erode',
        'phone': '9788796629'
    }

    return render_template('profile.html', user_details=user_details)

cart = []
purchase_history = []

product_durations = {}

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_details(product_id):
    if 'user_email' not in session:
        return redirect(url_for('login'))

    products = load_products()
    product = products[product_id]

    if request.method == 'POST':
        action = request.form['action']
        if action == 'add_to_cart':
            cart.append(product)  # Add product to cart
        elif action == 'buy':
            purchase_history.append(product)  # Add product to purchase history

    if 'start_time' in session:
        start_time = session['start_time']
        current_time = datetime.datetime.now().timestamp()
        duration = current_time - start_time

        if product_id in product_durations:
            product_durations[product_id] += duration
        else:
            product_durations[product_id] = duration
        del session['start_time']
    # else:
    # Store the start time in the session
    session['start_time'] = datetime.datetime.now().timestamp()

    return render_template('product_details.html', user_email=session['user_email'], product=product, product_id=product_id)

@app.route('/logout')
def logout():
    if 'user_email' in session:
        user_email = session['user_email']
        products = load_products()
        
        with open('user_visit_log.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            for product_id, duration in product_durations.items():
                product = products[product_id]
                product_status = 'Visited'
                
                if product in cart:
                    product_status = 'Added to Cart'
                elif product in purchase_history:
                    product_status = 'Bought'

                time_duration = 0.8 if product_status == 'Added to Cart' else (1.0 if product_status == 'Bought' else duration)
                
                csvwriter.writerow([user_email, product_id, product['product_name'], product_status, time_duration])
        
        session.pop('user_email', None)
        cart.clear()  # Clear the cart after logging
        product_durations.clear()  # Clear the product_durations dictionary
        
    return redirect(url_for('login'))

aCount = 0
bCount = 0
cCount = 0

@app.route('/', methods=['GET', 'POST'])
def chat_page():
    # Log writing code
    user_email = session['user_email']
    products = load_products()
    
    with open('user_visit_log.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        for product_id, duration in product_durations.items():
            product = products[product_id]
            product_status = 'Visited'
            
            if product in cart:
                product_status = 'Added to Cart'
            elif product in purchase_history:
                product_status = 'Bought'
            time_duration = 0.8 if product_status == 'Added to Cart' else (1.0 if product_status == 'Bought' else duration)
            
            csvwriter.writerow([user_email, product_id, product['product_name'], product_status, time_duration])
    
    cart.clear()  # Clear the cart after logging
    product_durations.clear()  # Clear the product_durations dictionary
        # Log writing code
    if request.method == 'POST':
        loading = True
        user_message = request.form['user_message']
        selected_mode = request.form['mode']

        global aCount
        global bCount
        global cCount

        bot_reply = 'NaN'

        delay = 0
        time.sleep(8)

        random_no = random.randint(1, 999914)

        try:
            if selected_mode == 'a':
                imgprompt = letaidecide(user_message)
                result = stablediffusion(imgprompt, seed=random_no)
            elif selected_mode == 'b':
                imgprompt = personalized(user_message)
                result = stablediffusion(imgprompt, seed=random_no)
            elif selected_mode == 'c':
                imgprompt = latesttrend(user_message)
                result = stablediffusion(imgprompt, seed=random_no)
            bot_reply = result
            loading = False
            delay = 0
        except ValueError:
            bot_reply = "Please enter a valid number."
            loading = False
            delay = 0

        return jsonify({'bot_reply': bot_reply, 'loading': loading, 'delay': delay})

    return render_template('generator.html')

def letaidecide(request):
    model = "tiiuae/falcon-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model)

    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
        max_length=200,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )

    llm = HuggingFacePipeline(pipeline=pipeline)
    return llm(request)

def getUserData():
        # Load user interactions data
    interactions_df = pd.read_csv('user_visit_log.csv')

    # Load products data
    products_df = pd.read_csv('products.csv')

    # Merge interactions and products data
    merged_df = interactions_df.merge(products_df, on='product_id')

    # Calculate average rating for each product
    product_avg_rating = merged_df.groupby('product_id')['rating_given_by_customer'].mean()

    # Create a user-product rating matrix
    user_product_ratings = merged_df.pivot_table(index='user_id', columns='product_id', values='rating_given_by_customer')

    # Fill NaN values with 0 (for products not interacted by users)
    user_product_ratings = user_product_ratings.fillna(0)

    # Apply Label Encoding to categorical attributes
    label_encoders = {}
    for column in ['pattern', 'occasion', 'brand', 'ideal_for', 'fabric', 'color']:
        le = LabelEncoder()
        products_df[column] = le.fit_transform(products_df[column])
        label_encoders[column] = le

    # Calculate cosine similarity between products based on attributes
    product_attributes = products_df[['pattern', 'occasion', 'brand', 'ideal_for', 'fabric', 'color']]
    cosine_sim = cosine_similarity(product_attributes, product_attributes)

    # Define a function for collaborative and content-based recommendations
    def get_recommendations(user_id):
        user_ratings = user_product_ratings.loc[user_id]

        # Collaborative Filtering: Find products similar to those rated positively
        collaborative_recommendations = user_product_ratings.columns[user_ratings > 0]

        # Content-Based Filtering: Sort products based on average rating and attributes
        content_based_recommendations = product_avg_rating.index.tolist()
        content_based_recommendations.sort(key=lambda x: (product_avg_rating[x], -user_ratings[x]))

        return collaborative_recommendations, content_based_recommendations

    # Example user ID
    example_user_id = 1

    collaborative_recs, content_based_recs = get_recommendations(example_user_id)

    # print(f"Collaborative Filtering Recommendations:")
    # for idx, rec in enumerate(collaborative_recs, start=1):
    #     print(f"{idx}. Product ID: {rec}")


    content_based_filtering=[]
    print(f"\nContent-Based Filtering Recommendations:")
    for idx, rec in enumerate(content_based_recs, start=1):
        # print(f"{idx}. Product ID: {rec}")
        content_based_filtering.append(rec)

    print("Top rated content_based_filtering")
    print(content_based_filtering)

    # ---------------------------------
    products_df = pd.read_csv('products.csv')

    import random

    num_combinations = 15
    combination_length = 6
    print(" ")
    for _ in range(num_combinations):
        # random combination of top 5 product id's 6 times, coz. i'm expecting to get random of the top5 most preferred product's 
        # 6 attributes. 15 is the total no of such combinations i need
        random_combination = random.sample(content_based_filtering, combination_length)
        print(random_combination)
        # below code is used to get the values of those attributes from the corresponding cells of that sheet
        product_attributes = {}
        attr = ['pattern','occasion','brand','ideal_for','fabric','color']
        final=[]
        count=0
        for product_id in random_combination:
            row = products_df[products_df['product_id'] == product_id]
            if not row.empty:
                valueneeded = row.iloc[0][attr[count]]
                # print(valueneeded)
                count+=1
                final.append(valueneeded)

        return final

def personalized(request):
    model = "tiiuae/falcon-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model)

    userdata= getUserData()
    userlist = ','.join(userdata)

    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
        max_length=200,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )

    llm = HuggingFacePipeline(pipeline=pipeline)
    return llm(request+userlist)

def latesttrend(request):
    model = "tiiuae/falcon-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model)
    
    a=get_trends(request)

    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
        max_length=200,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )

    llm = HuggingFacePipeline(pipeline=pipeline)
    return llm(request+a)


def get_trends(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    data_list = []
    bold_elements = soup.find_all("b")
    for bold_element in bold_elements:
        span_elements = bold_element.find_all("span")
        for span_element in span_elements:
            data_list.append(span_element.get_text(strip=True))

    return data_list

if __name__ == "__main__":
    url = "https://www.fibre2fashion.com/industry-article/9076/36-best-current-fashion-trends"  # Replace with the actual URL
    extracted_data = get_trends(url)

    if extracted_data:
        print("Data extracted from <span> tags within <bold> tags:")
    else:
        print("No data extracted.")


if __name__ == '__main__':
    app.run(debug=True)


