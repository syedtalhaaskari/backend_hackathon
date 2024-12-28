## Project Description and Features
A simple job listing application
User can have one role i.e. Job_Seeker or Employer.
Employer can post, edit and delte their posted jobs.
Employer can see number of applicants.
Employer can change applicant status

Job_Seeker can apply for multiple jobs.
Anyone can view jobs but to apply or to view salary range login is necessary.

One employer cannot view another employer's job applicants.

User can edit their profile.

## How to Run
1. Install dependencies\
`pip install -r requirements.txt`
2. Change directory\
`cd job_portal`
3. Run application\
`python manage.py runserver`

**Note**: Forgot password API is not visible in swagger but exist in the application http://127.0.0.1:8000/auth/password_reset/

