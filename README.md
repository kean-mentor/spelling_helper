# spelling_helper
A simple Flask web application to practice j/ly spelling

Usage:
--
* create a virtualenv
* activate the virtualenv
* install the requirements
* export FLASK_APP=spelling_helper.py
* export FLASK_ENV=development (optional)
* flask run

In the app you can practice the spelling of hungarian words with j/ly.

**Notes:**
* If you want to practice with more words than currently in the database, then you automatically redirected to the 'word manage' page
* You can't add words without j or ly to the list (but there is no visual feedback if you try to add one)
* You can't add duplicate words (missing visual feedback here also)
