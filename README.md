# amplify-elb-blog
Amplify - Elastibeanstalk - Demo


## How to build the backend locally

Here are the following instructions to launch the backend : 

̀```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
̀```

Then to launch the backend : 

```bash
FRONTEND_URL=http://localhost:4321 fastapi dev api.py
```

You should see the following output : 

```bash
Serving at: http://127.0.0.1:8000               
API docs: http://127.0.0.1:8000/docs            
Running in development mode, for production use:
fastapi run    
```

### Updating the dependencies

```bash
pipreqs . --force
```



