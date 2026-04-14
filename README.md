# DeployHub

## Members
- Dylan Collins(124385793) - GitHub: negligent430
- Eoin Walsh (124485562) - GitHub: 124485562-spec
- Luke Delaney (124416056) - GitHub: Luke16056
- John Terce (124420722) - GitHub: JT575

## Live Link
https://is2209-2.onrender.com/home

## Demo Steps
1. Visit https://is2209-2.onrender.com/
2. Search for a breed e.g. "labrador"
3. Click the 🎲 button for a random breed
4. Visit `/status` to see service health
5. Visit `/logs` to see application activity
6. Visit `/health` to see JSON health check

## Run Locally
1. Clone the repository
2. cd IS2209-2
3. pip install -r requirements.txt
4. Create a .env file using .env.example as a template
5. flask run
Note: You will need to create your own .env file

## Enviormental Variables
- SUPABASE_URL=
- SUPABASE_KEY=
- DOG_API=
- SECRET_KEY=

### Requirements
- Python 3.11+
- Docker
- A Supabase account

## Endpoints
- /
- /home
- /breed/<id>
- /random
- /health
- /status
- /logs

## CI/CD
- GitHub Actions runs on every PR and push to main
- Pipeline: install → lint → tests → Docker build → push to GHCR
- Auto deploys to Render.io on merge to main

## External Documentation
- Python Offical Docs for requests -> https://pypi.org/project/requests/
- Supabase Offical Docs for Python -> https://supabase.com/docs/reference/python/installing
- Github Docs -> https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
- W3Schools Tables -> https://www.w3schools.com/html/html_tables.asp
