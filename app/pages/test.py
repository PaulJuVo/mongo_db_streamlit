import streamlit as st



def get_user_name():
    '''Tetst doc string'''
    return 'John'

with st.echo():
    # Everything inside this block will be both printed to the screen
    # and executed.

    def get_punctuation():
        return '!!!'

    greeting = "Hi there, "
    value = get_user_name()
    punctuation = get_punctuation()

    st.write(greeting, value, punctuation)

# And now we're back to _not_ printing to the screen
foo = 'bar'
st.write('Done!')

class Dog:
  '''A typical dog.'''

  def __init__(self, breed, color):
    self.breed = breed
    self.color = color

  def bark(self):
    return 'Woof!'


fido = Dog("poodle", "white")

st.help(fido)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

def out_button():
    st.session_state.clicked = False

st.button('Click me', on_click=click_button)
st.button('out', on_click=out_button)

if st.session_state.clicked:
    # The message and nested widget will remain on the page

    st.write('Button clicked!')
    st.slider('Select a value')