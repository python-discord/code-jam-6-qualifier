# Kivy Application Qualifier

- **Deadline:** 2020-01-10 12:00 UTC
- **Submission form:** https://forms.gle/MzzZs9mFMKe2bwP77
- **Theme suggestions:** https://forms.gle/ejkha9bF6kKjnRJJA

This qualifier task for the upcoming [Winter Code Jam](https://pythondiscord.com/pages/code-jams/code-jam-6/) is to write a Kivy application in which the end user can move around an image on screen. Use [this image](https://github.com/python-discord/branding/blob/master/logos/logo_discord/logo_discord_256.png) as the default image, so we can your code using the same image you've used while creating your application.

To get you started, we've set up a very basic "Hello World!" app in the [`qualifier.py`](qualifier.py) file that you can use as a base for your app.


### Basic Requirements

- Create a Kivy application that allows the user to move around an image on screen with the arrow keys

### Advanced requirements

- Allow the user to zoom in/zoom out on the image using the `w` and `s` keys

- Allow the user to load a different image from disk

- Add support for using a mouse (or touch!) to interact with your image

- Any other fun addition that you can think of!

### Code Style & Readability
While not a hard requirement, we will take code style and readability into account when judging submissions for both the qualifier as well as the code jam itself. Please try to keep your code readable for yourself and others, and try to comply with [PEP 8](https://www.python.org/dev/peps/pep-0008/). To check if your code follows PEP 8, we will use a tool called [flake8](http://flake8.pycqa.org/en/latest/) configured with a maximum line length of 100. If you want to run flake8 yourself, you can use `flake8 --max-line-length=100 /path/to/code` to run it with the same settings as we will use. (Note: you will need to [install flake8](http://flake8.pycqa.org/en/latest/index.html#installation) first.)

## Notes
- **Please note that the qualifier task is supposed to be an individual challenge.** This means that you should not discuss (parts of) your solution to the qualifier task in public (including our server) and that you should try to solve it individually. Obviously, this does not mean that you can't do research or ask questions about the Python concepts you're using to solve the qualifier, but try to use general examples when you post code during this process.

- Since you can only submit your code and no assets, use `logo_discord_256.png` as the default image. We'll make sure to run your code with that image available in the same directory as your script, so specify it using a relative path.
