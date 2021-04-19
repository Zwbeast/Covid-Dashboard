# Covid-Dashboard

## Description

Mary is a GWU student. She is very concerned with COVID. She wants to have an app that she can monitor her health status for any sign of COVID. Among other features, she wants to be able to:
- Log for any symptom related to COVID that she may have experimented, e.g., fever, coughing, etc. For instance, on Dec 1st, 10:00 AM EST, Mary measured her temperature and found out that the was 80F. On Dec 2nd, Mary had a cough that was upsetting her (you can use https://melbentgroup.com.au/wp-content/uploads/2015/10/MEG-Cough-Severity-Index-CSI.pdf for cough severity values)
- Sync with her fitbit, iphone, or Apple Watch so she could have in a single app not only her own diagnostic but also her activities such as running, steps per day, etc.
- Log any medicines that she is currently taking. For instance, Mary is taking 5mg of Vitamin D per day.
- Log doctor visits, e.g., Mary want to her ophthalmologist on Dec 2nd
- Log her trips, e.g., Mary went to Cancún, MX, during thanksgiving and stay there for 3 days. She had a lot of fun!
- Log news from her friends and family, e.g., Joe, a former Mary’s boyfriend, told her he tested positive for COVID on Dec 5th. Mary is concerned since she met Joe last time on Dec 4th. They had dinner together in a very well know restaurant close to GWU: they sat indoors.
-	Log her take outs. Mary does not like to cook. She always eat out. Due to COVID, she frequent asks for takeout’s in several restaurants around GWU.
- Finally, Mary wants to have access to her dashboard indicating the like hood she was exposed to COVID given all the information she has collected about her life style.

Students are free to add new capabilities to the app.

## Indicator

We use a simple strategy to roughly estimate the probability of getting COVID-19. Normally, the more activities people have, the higher risk they would get. Thus, we retrieve all the logs a user has. Then, we calculate a total score by summing each activity score (Logically speaking, high-risk activities would have higher scores). The higher total score users have, the greater probability they get.

We divide risk into 5 levels:

- Very low

- Low

- Medium 

- High

- Extremely high

Users can enter the Indicator page to get their own probablities (At least they have some log records).

## How to run:

Under Covid-Dashboard directory, not under dashboard directory

On Mac:
```
export FLASK_APP=dashboard
export FLASK_ENV=development
flask init-db
flask run
```
On Windows:
```
set FLASK_APP=dashboard
set FLASK_ENV=development
flask init-db
flask run
```

## Use Case Diagram
<img src="https://i.ibb.co/GVyH1MC/Picture1.png" alt="Picture1" border="0" width="800" height="800">

## Domain Class Model
<img src="https://i.ibb.co/NSNk5Sr/Picture2.png" alt="Picture2" border="0" width="800" height="800">
Have fun :)
