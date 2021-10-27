import streamlit as st
from PIL import Image
import os


def app():
	st.title("Cellular Automata")
	st.write("""
		An exploration done as part of the final project for
		Theory of Computation (Spring 2020) offered by Prof. Mahavir Jhawar
		""")
	st.markdown("---")

	st.write("""
		## An Introduction to Cellular Automata
		
		Cellular Automata are simple machines that are capable of producing complex patterns/behaviors based
		on simple rules of interaction between its elements. This app will allow you to play around with 
		elementary cellular automata, the density classification problem and automata that can be used to solve it
		and some cool applicaitons of these automata in physical systems.

		Elementary cellular automata are $1$-D automata based on all $256$ possible rules of evolution when interaction
		is limited to the $2$ nearest neighbours. Below, we show how we represent these rules for implementation purposes.


		""")
	im_path = os.path.join(os.path.dirname(__file__), 'images/picCA1.png')
	img = Image.open(im_path)
	st.image(img, caption="elementary rules")

	st.write("""
		
		We primarily explore automata whose individual cells can be in either of $2$ states - here, $0$ and $1$.
		Therefore, at each timestep of evolution, we can think of our automata as fully specified by a "state array" where each cell
		has one of the $2$ possible states, and the transition rule applied at each cell. The state array produced as a result of "evolving" the current state array
		represents the successor generation. To observe how generations change with time (i.e, dynamically), we can stack the state arrays vertically with the oldest generation 
		at the top and successively newer generations at the bottom, to obtain an image where each pixel is either black or white. 
		""")
	im_path = os.path.join(os.path.dirname(__file__), 'images/explanationPlot.png')
	img = Image.open(im_path)
	st.image(img, caption="an explanation of our output format")

	st.write("""
		
		Evidently, the final image will show some emergent pattern, and these patterns depend not just on the rules of transition applied, but also 
		the initial state array, which we will henceforth refer to as the Initialization Vector (IV). Some rules are interesting and others are boring, 
		in that the patterns either converge, oscillate or show chaotic behavior. Those that converge can be thought of as destructive in nature, as no matter what 
		the IV configuration is, it will take on the same state in all cells after a certain number of evolutions. Some show very complex patterns that either repeat recursively
		forming fractals, or show oscillatory dynamics. Others show completely random behavior. Some rules even show superposability on with respect to some operation (such as AND, OR, XOR, NOT).

		Here are a few examples of patterns generated using elementary automata, with the respective rules that generated them. To make it uniform, we have used the same IV in all of them. 

		""")

	im_path = os.path.join(os.path.dirname(__file__), 'images/showcase1.png')
	img = Image.open(im_path)
	st.image(img, caption="a few patters we generated 1.0")

	im_path = os.path.join(os.path.dirname(__file__), 'images/showcase2.png')
	img = Image.open(im_path)
	st.image(img, caption="a few patterns we generated 2.0")
	
	st.markdown("For more details and definitions, you can take a look at this [report](https://github.com/shw3ta/Cellular-Automata/blob/main/documents/CS_2349___Theory_of_Computation__Final_Report.pdf).")

	st.markdown("""---""")

	# st.markdown("""
	# <embed src="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf" width="700" height="600">
	# """, unsafe_allow_html=True)

	im_path = os.path.join(os.path.dirname(__file__), 'images/pyramids.png')
	img = Image.open(im_path)
	st.image(img, caption="your neighbours define you")
	st.markdown("""---""")
