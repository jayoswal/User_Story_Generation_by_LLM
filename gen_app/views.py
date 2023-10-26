from django.shortcuts import render
from django.http import HttpResponseRedirect
from gen_app.models import InputForm
import openai
import json
from django.conf import settings


def index(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            inp_prompt = form.cleaned_data['inp_prompt']

            # generate the json_data - START

            openai.api_key = settings.OPEN_AI_API_KEY

            messages = [
                {"role": "system", "content": """You will be given a software requirement text. Generate User stories from it and provide the output as array of JSON wiith the keys being User_Story_Number, Title, Main_Actor, Action_Verb, System_Entity, Entire_User_Story.""" },
                {'role': 'user', 'content': inp_prompt}]

            # Try with different models.
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages
            )   

            content = response["choices"][0]["message"]["content"]
            json_data = json.loads(content)

            # generate the json_data - END
            
            # Store the JSON data in the session
            request.session['json_data'] = json_data
            
            # Redirect to the results page
            return HttpResponseRedirect('results/')
    else:
        form = InputForm()
        json_data = {}
    return render(request, 'index.html', {'form': form, 'json_data': json_data})

def results(request):
    # Retrieve the JSON data from the session
    json_data = request.session.get('json_data', {})
    return render(request, 'results.html', {'json_data': json_data})
