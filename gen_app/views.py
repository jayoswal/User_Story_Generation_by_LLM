from django.shortcuts import render
from django.http import HttpResponseRedirect
import openai
import json
from django.conf import settings
from .forms import TextInputForm


def index(request):
    if request.method == 'POST':
        form = TextInputForm(request.POST, request.FILES)
        if form.is_valid():
            inp_prompt = form.cleaned_data['inp_prompt']
            file_inp_prompt = form.cleaned_data.get('file_input')
            if inp_prompt and file_inp_prompt:
                form.add_error(None, 'Enter either text or upload file.')
            elif not inp_prompt and not file_inp_prompt:
                form.add_error(None, 'Text input or file upload is required.')
            elif file_inp_prompt and not file_inp_prompt.name.endswith('.txt'):
                form.add_error('file_input', 'Invalid file type. Only .txt files are allowed.')
            elif inp_prompt:
                # do nothing
                pass
            elif file_inp_prompt:
                with file_inp_prompt.open() as file:
                    file_content = file.read().decode('utf-8')
                # fix the prompt
                inp_prompt = file_content

   
            
            # generate the json_data - START

            openai.api_key = settings.OPEN_AI_API_KEY

            messages = [
                {"role": "system", "content": """You will be given a software requirement text. Generate User stories from it and provide the output as array of JSON wiith the keys being User_Story_Number, Title, Main_Actor, Action_Verb, System_Entity, Entire_User_Story. Entire_User_Story should be in the format As a [Main_Actor] I want to [Action_Verb] so that [benefit]""" },
                {'role': 'user', 'content': inp_prompt}]

            # Try with different models.


            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                max_tokens=600,
                temperature=0.2
            )   

            answer = response["choices"][0]["message"]["content"]



            json_data = json.loads(answer)

            # generate the json_data - END
            
            # Store the JSON data in the session
            request.session['json_data'] = json_data
            
            # Redirect to the results page
            return HttpResponseRedirect('results/')
    else:
        form = TextInputForm()
        json_data = {}
    return render(request, 'index.html', {'form': form, 'json_data': json_data})

def results(request):
    # Retrieve the JSON data from the session
    json_data = request.session.get('json_data', {})
    return render(request, 'results.html', {'json_data': json_data})
