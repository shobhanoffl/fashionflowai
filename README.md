  Introduction
Introducing "FashionFlowAI": Your Ultimate Conversational Fashion Outfit Generator In the dynamic world of fashion, where style evolves at the speed of a click, Flipkart presents a revolutionary solution that transcends traditional product discovery. Enter "FashionFlowAI," our cutting-edge Conversational Fashion Outfit Generator powered by GenAI. Embracing the transformative capabilities of Generative AI, FashionFlowAI redefines the way users engage with fashion, ushering in a new era of personalized outfit curation through natural, human-like conversations.


Flow of Working
1. Once a new account is created, the user will have the option to fill the basic details, which is mandatory for users of FashionFlowAI Generator, and not the ecommerce

2. It all starts with the usage of the ecommerce portal. This generates a variety of data, starting from the interation of the user with the products, amount of time spent, products added to the cart and much more.

3. Once the user enters the FashionFlowAI Generator, the user will be given with 3 modes, each having it's own features - Let AI Decide, Personalized and Latest Design

4. Whenever the user is convinced with the fashion costume design, the user will be listed with the Flipkart Product Link for each of the products, accessories, fashion costumes used in the design. The user may either buy those, or can Create a order of that Fashion Costumer to a Fashion Designer

Further info is provided below

Data Collection
FashionFlowAI Generator
FashionFlowAI Architecture

Data Collection
Data Collection happens in various stages. They are,

Products that are added to the cart
Products purchased
Products visited or viewed
User's details or preferences that are filled in their profile - This data is made to use only after users agree to the Terms, Conditions and Usage Rights
User's preferences are collected using Collaborative Filtering
User's Social Media Insights - using Meta's Graph API

FashionFlowAI Generator
It is an integrated system, where the requests from the user is passed to the architecture of models and the image of the fashion design is returned as response. It includes 3 modes, each with it's own individual functionality. They're 'Let AI Decide', 'Personalized', 'Latest Design'.

Let AI Decide - Here, the architecture generates generalized output, with most appropritate and suitable combinations
Personalized - The game changer of this product is here - the input for the model not just includes the request of the user, but also their preferences/favourites for Colour, Brand, Occasion, Fabric, Pattern with Social Media Insights from Graph API. These combinations result in much more personalized outfit to be getting generated
Latest Design - Latest fashion trends and new costumes are derived from the internet using web scraping (using BeautifulSoup in Python) and is combined with the user input to generate a better fashion costume
Additional details include,

Each image has a detailed description about it, along with the accessories and fashion costumes involved
Each image is accompanied with a 'Buy now' Link, which redirects to the screen of choosing to buy those products or to order to a Fashion Designer
Each Prompt-Response Set is a conversational data, that can be used in the further conversations with the model
User's Social Media Insights - using Meta's Graph API

FashionFlowAI Architecture
FashionFlowAI is construcuted using two parts, where both of them are open-source and commercially usable models, making it more appropriate for our product. It involves,

A Falcon-7b-instruct, a causal decoder-only model built by TII based on Falcon-7B and finetuned on a mixture of chat/instructions, which is used to construct image prompts from the user input. It relies on the pre trained weights, that makes it suitable for image prompt generation.
And Stable Diffusion, a deep learning, text-to-image model, which is again relies on a pre-trained weight of various, vernacular costumes.
The prompt that is generated from Falcon-7b-instruct is then passed to Stable Diffusion, to generate the image


Site Map
Configuration
- Profile
Ecommerce
- Fashion
- Electronics
- Cart
AI Fashion Generator
- FashionFlowAI

Terms and Conditions
Terms and Conditions: Our Terms and Conditions outline the agreement between users and our company regarding the utilization of their shopping cart and purchase history data to enhance their shopping experience. Users' consent is obtained to collect and process this data for tailored shopping recommendations. No sensitive personal information is collected, only cart items and purchase history from our platform. Data security is ensured through protective measures, and third-party sharing is not allowed without explicit consent. Users retain control over their data and can opt-out of personalized suggestions. Account deletion results in data removal. We reserve the right to update these terms, and any changes are effective upon posting on our website. Users who continue to use our services accept these terms.
