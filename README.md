# Welcome to [Lo-Fi Converter GUI!](https://youtube-lofi.streamlit.app/)
Simple way to convert **Youtube** Song to Lo-Fi version of that song just from its url !!!

# Footer and BuyMeACoffee button
st.markdown("""
        <h10 style="text-align: center; position: fixed; bottom: 3rem;">Developed <a href='https://lequocthai.com'>Lê Quốc Thái</a> | <a href='mailto:lequocthai@gmail.com'>lequocthai[at]gmail.com</a> | <a href='https://t.me/tnfsmith'>Telegram</a> | <a href='tel:0985010707'>Zalo</a> </h10>""",
        unsafe_allow_html=True)
button = """<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="LeQuocThaiy" data-color="#FFDD00" data-emoji="🥤" data-font="Cookie" data-text="Buy me a Coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>"""
html(button, height=70, width=225)
st.markdown(
        """
        <style>
            iframe[width="225"] {
                position: fixed;
                bottom: 35px;
                right: 40px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
## Contributions are appreciated 👍
Hosted on Streamlit
