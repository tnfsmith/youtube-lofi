import os
import streamlit as st
import music
import yt_dlp
import uuid
from streamlit.components.v1 import html, components


# Function to delete temporary audio files
def delete_temp_files(audio_file, output_file, mp3_file):
    os.remove(audio_file)
    os.remove(output_file)
    if mp3_file:
        os.remove(mp3_file)


@st.cache_data(show_spinner=False, max_entries=5)

def isDownlaodable(youtube_link):
    
    try:
        with yt_dlp.YoutubeDL({'format': 'bestaudio', "quiet":True, "noplaylist":True}) as ydl:
            dur = None
            info_dict = ydl.extract_info(youtube_link, download=False)
            for i in info_dict['formats']:
                if "duration" in i['fragments'][0].keys():
                    dur = i['fragments'][0]["duration"]
                    break

    except Exception as e:
        st.error("Make sure Youtube video is publicly globally avilable!!!")
        st.error(e)
        print(f"ERROR: {e} ==> {youtube_link}")
        return False
    if dur <= 12000: #600
        return True
    else:
        st.error("Make sure Youtube song less than 200 minutes (about 3.33 hours)")
        return False

# Function to download YouTube audio and save as a WAV file
@st.cache_data(max_entries=4)
def download_youtube_audio(youtube_link):
    uu = str(uuid.uuid4())

    if isDownlaodable(youtube_link):
        try:
            with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': 'uploaded_files/' + uu + '.%(ext)s', "quiet":True, "noplaylist":True}) as ydl:
                info_dict = ydl.extract_info(youtube_link, download=True)
                audio_file = ydl.prepare_filename(info_dict)
                song_name = info_dict['title']
            print(f"Downloaded YouTube link: {youtube_link} ==> {song_name}")
            mp3_file_base = music.msc_to_mp3_inf(audio_file)
            return (audio_file, mp3_file_base, song_name)
        except Exception as e:
                st.error("Error")
                print(f"ERROR: {e} ==> {youtube_link} in download_youtube_audio")
        return None

# Main function for the web app
def main():
    st.set_page_config(page_title="Youtube Audio Lofi Converter", page_icon=":microphone:", layout="wide", )
    
    st.title(":microphone: Youtube Audio Lofi Converter (Lossless Audio)")
    st.info("🌟 Auto download audio at 320kbps. New features is still development for best user experience. 🎉 Tip: Use Headphone for best experience :headphones:")
    #st.info("Tip: Use Headphone for best experience :headphones:")
    if 'processed_audio_data' not in st.session_state:
        st.session_state['processed_audio_data'] = None
    # Select bitrate
    #bitrate_options = ['192k', '256k', '320k']
    #selected_bitrate = st.selectbox("🎧 Select MP3 Bitrate: 🎧", bitrate_options, index=2)  # Default to highest quality

    with st.form(key='youtube_link_form'):
            youtube_link = st.text_input("🔎 Enter the YouTube link 🔗 of the song to convert: Example URL below Ai muốn nghe không - Đen Vâu", value="https://www.youtube.com/watch?v=JxBnLmCOEJ8", help="Example this URL Ai muốn nghe không - Đen Vâu")
            #youtube_link = st.text_input("Enter the YouTube link 🔗 of the song to convert:", placeholder="https://www.youtube.com/watch?v=JxBnLmCOEJ8") #Den Vau
            #process_button = st.button("Process Audio")
            submit_button = st.form_submit_button(label='💯 Process Audio 🔃')

    

    if submit_button and youtube_link:
        duration = 0  # Initialize duration
        try:   # Download audio from YouTube link and save as a WAV file (using cached function)
            d = download_youtube_audio(youtube_link)
            print(f"Retreaving YouTube link: {youtube_link}")
            if d:
                audio_file, mp3_base_file, song_name = d
                # Download button for the original audio mp3 before convert to.wav file
                st.session_state['processed_data'] = (audio_file, mp3_base_file, song_name)
            else:
                if st.session_state['processed_data']:
                    audio_file, mp3_base_file, song_name = st.session_state['processed_data']
            if st.session_state['processed_data']:    
                st.download_button(
                    label="💾 Download Original Youtube Audio 🎵",
                    data=mp3_base_file,
                    file_name=f"{song_name}.mp3",
                    mime="audio/mp3"
                )
                # Show original audio
                st.write("🎶 Original Downloaded Youtube Audio (.wav). Click play button to listen:")

                st.audio(mp3_base_file, format="audio/mp3")
                # Download button for the original audio
                #st.download_button(
                #    label="💾 Download Original Youtube Audio 🎵",
                #    data=mp3_base_file,
                #    file_name=f"{song_name}.mp3",
                #    mime="audio/mp3"
                #)
                
                # Get user settings for slowedreverb function
                if duration <=1200: # 1200 seconds == 20 minutes
                    room_size, damping, wet_level, dry_level, delay, slow_factor = get_user_settings()

                    # Process audio with slowedreverb function
                    output_file = os.path.splitext(audio_file)[0] + "_lofi.wav"
                    print(f"🎯 User Settings: {audio_file, output_file, room_size, damping, wet_level, dry_level, delay, slow_factor}")
                    music.slowedreverb(audio_file, output_file, room_size, damping, wet_level, dry_level, delay, slow_factor)

                    # Show Lofi converted audio
                    st.write("🎶 Youtube Audio Lofi Converted Audio (🔉 Listenning Preview Below)")
                    st.audio(music.msc_to_mp3_inf(output_file), format="audio/flac") #audio/mp3
                    
                    st.info (":fire::fire::fire:Note: Due to original Youtube Audio support, audio quality after converted may depend on it :smile:")
                    st.download_button("🎵 Download Lofi Lossless Audio (.flac) 💾", music.msc_to_mp3_inf(output_file), song_name+"_lofi.flac") #_lofi.mp3
                else:
                    st.info("The video is longer than 20 minutes. Reverb processing is skipped.")
        except Exception as e:
               st.error(f"An error occurred: {e}")
                #print("Error occcored in code")
               st.warning("Error Try again")

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

# Function to get user settings
def get_user_settings():
    advanced_expander = st.expander("🎼 Advanced Settings 👏")
    with advanced_expander:
        st.write("Adjust the parameters for the slowedreverb function:")
        room_size = st.slider("Reverb Room Size", min_value=0.1, max_value=1.0, value=0.75, step=0.1)
        damping = st.slider("Reverb Damping", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
        wet_level = st.slider("Reverb Wet Level", min_value=0.0, max_value=1.0, value=0.08, step=0.01)
        dry_level = st.slider("Reverb Dry Level", min_value=0.0, max_value=1.0, value=0.2, step=0.01)
        delay = st.slider("Delay (ms)", min_value=0, max_value=20, value=2)
        slow_factor = st.slider("Slow Factor", min_value=0.0, max_value=0.2, value=0.08, step=0.01)
    return room_size, damping, wet_level, dry_level, delay, slow_factor

if __name__ == "__main__":
    main()
