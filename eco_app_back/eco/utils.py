from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder
from .models import UserHabit, Habit, Advice, Category, VectorStore, UserPlan, Favorite, UserChallenge
import numpy as np
from scipy.sparse import hstack
import pickle

def create_vec():
    advices_description = Advice.objects.values_list('description', flat=True)
    vector = TfidfVectorizer()
    vector.fit(list(advices_description))
    category_code = OneHotEncoder(sparse_output=True)
    category_list = Category.objects.values_list('title', flat=True)
    category_code.fit(np.array(list(category_list)).reshape(-1, 1))

    advice_d_vector, created = VectorStore.objects.get_or_create(title='TFIDF-description')
    category_vector, created = VectorStore.objects.get_or_create(title='OH-category')
    advice_d_vector.save_vec(vector)
    category_vector.save_vec(category_code)

def personal_advices(user):
    user_plans = UserPlan.objects.filter(user=user)
    user_challenges = UserChallenge.objects.filter(user=user)
    user_advices = Favorite.objects.filter(user=user, favorite_type='A')
    user_advices_id = user_advices.values_list('advice_id', flat=True)
    user_guides = Favorite.objects.filter(user=user, favorite_type='G')
    user_description=[]
    user_categories=[]
    for plan in user_plans:
        habits = UserHabit.objects.filter(plan=plan)
        for habit in habits:
            habit_description = habit.habit.description
            habit_category = habit.habit.category.title
            user_description.append(habit_description)
            user_categories.append(habit_category)
    for challenge in user_challenges:
        challenge_description = challenge.challenge.description
        challenge_category = challenge.challenge.category.title
        user_description.append(challenge_description)
        user_categories.append(challenge_category)
    for advice in user_advices:
        advice_description = advice.advice.description
        advice_category = advice.advice.category.title
        user_description.append(advice_description)
        user_categories.append(advice_category)
    for guide in user_guides:
        guide_description = guide.guide.description
        guide_category = guide.guide.category.title
        user_description.append(guide_description)
        user_categories.append(guide_category)
    print(user_description)
    print(user_categories)
    advices = Advice.objects.exclude(id__in=user_advices_id)
    advices_text = []
    advices_categories = []
    for advice in advices: 
        advices_text.append(advice.description)
        advices_categories.append(advice.category.title)
    print(advices_categories)
    print(advices_text)
    if user_description:
        advices_store = VectorStore.objects.get(title='TFIDF-description')
        vector = advices_store.get_vec()
        category_store = VectorStore.objects.get(title='OH-category')
        category_code = category_store.get_vec()
      
        advices_d_vector = vector.transform(advices_text)
        user_d_vector = vector.transform(user_description)
        advices_c_vector = category_code.transform(np.array(advices_categories).reshape(-1, 1))
        user_c_vector = category_code.transform(np.array(user_categories).reshape(-1, 1))
        user_vector = hstack([user_d_vector, user_c_vector]).toarray()
        mean_user_vector = user_vector.mean(axis=0)
        advices_vector = hstack([advices_d_vector, advices_c_vector]).toarray()
        similar = cosine_similarity(mean_user_vector.reshape(1, -1), advices_vector).flatten()
        
        sim_id = similar.argsort()[::-1][:3]
        dis_id = similar.argsort()[:3]

        sim_advices = []
        dis_advices = []

        for i in dis_id:
            dis_advices.append(advices_text[i])
        
        for i in sim_id:
            sim_advices.append(advices_text[i])

        advices_s = Advice.objects.filter(description__in = sim_advices)
        advices_d = Advice.objects.filter(description__in = dis_advices)

        return advices_s, advices_d
    else:
        return '', ''

