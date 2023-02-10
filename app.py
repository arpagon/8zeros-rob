#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# imap-bills-exporter/main.py
# Copyright 2022 Sebastian Rojo <arpagon@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = "Sebastian Rojo"
__copyright__ = "Copyright 2022, Sebastian Rojo"
__credits__ = []
__license__ = "Apache 2.0"
__version__ = "0.1.1"
__maintainer__ = "Sebastian Rojo"
__email__ = ["arpagon at gmail.com"]
__status__ = "beta"


import numpy as np
import scipy.io.wavfile
import streamlit as st
import streamlit.components.v1 as components
import replicate

model = replicate.models.get("riffusion/riffusion")
version = model.versions.get("8cf61ea6c56afd61d8f5b9ffd14d7c216c0a93844ce2d82ac1c9ecc9c7f24e05")

def genrate_riffusion(prompt_a):
    """Generates a wave with the given prompt

    Args:
        prompt_a (string): The prompt for the first wave.

    Returns:
        output(json): A json object representing the generated wave.
    """
    inputs = {
        # The prompt for your audio
        'prompt_a': prompt_a,

        # How much to transform input spectrogram
        # Range: 0 to 1
        'denoising': 0.75,

        # The second prompt to interpolate with the first, leave blank if no
        # interpolation
        # 'prompt_b': ...,

        # Interpolation alpha if using two prompts. A value of 0 uses prompt_a
        # fully, a value of 1 uses prompt_b fully
        # Range: 0 to 1
        'alpha': 0.5,

        # Number of steps to run the diffusion model
        # Minimum: 1
        'num_inference_steps': 50,

        # Seed spectrogram to use
        'seed_image_id': "vibes",
    }

    # https://replicate.com/riffusion/riffusion/versions/8cf61ea6c56afd61d8f5b9ffd14d7c216c0a93844ce2d82ac1c9ecc9c7f24e05#output-schema
    output = version.predict(**inputs)
    return output


def generate_sine_wave(frequency, duration, sample_rate):
    """Generates a sine wave with the given frequency, duration, and sample rate.

    Args:
        frequency (float): The frequency of the sine wave in Hz.
        duration (float): The duration of the sine wave in seconds.
        sample_rate (int): The number of samples per second.

    Returns:
        numpy.ndarray: A numpy array representing the generated sine wave.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)
    return wave.astype(np.float32)

def write_wave_file(filename, wave, sample_rate):
    """Writes a wave to a WAV file with the given filename and sample rate.

    Args:
        filename (str): The name of the file to write.
        wave (numpy.ndarray): The wave data to write to the file.
        sample_rate (int): The number of samples per second.
    """
    scipy.io.wavfile.write(filename, sample_rate, wave)

def main():
    st.set_page_config(
        page_title="8zer0s",
        page_icon=":microphone:",
        layout="wide"
    )
    
    tab1, tab2 = st.tabs(["Generate", "DAW"])

    st.sidebar.image("assets/img/logo_300dpi.png", width=300, caption="Logo")

    frequency = st.sidebar.slider("Frequency (Hz)", 0.0, 22050.0, 440.0)
    duration = st.sidebar.slider("Duration (s)", 0.0, 10.0, 1.0)
    sample_rate = st.sidebar.slider("Sample Rate (Hz)", 44100, 48000, 44100)

    wave = generate_sine_wave(frequency, duration, sample_rate)

    with tab1:
        st.header("Generate sine wave")

        # add text box to enter a prompt
        prompt = st.text_input("Enter a prompt")

        if st.button("Generate Wave"):
            filename = "assets/audios/generate/sine_wave_{:.0f}Hz_{:.0f}s.wav".format(frequency, duration)
            write_wave_file(filename, wave, sample_rate)
            st.success("Generated wave file: {}".format(filename))

            # add st.audio to play the wave
            st.audio(filename, format="audio/wav", start_time=0)
        
        if st.button("Generate via AI"):
            output=genrate_riffusion(prompt_a=prompt)
            st.success(output)

            # add st.audio to play the wave
            # st.audio(filename, format="audio/wav", start_time=0)
    
    with tab2:
        # add iframe component
        st.header("DAW")
        components.iframe("https://gridsound.com/daw/",height=800)

    #data = requests.get("https://jsonplaceholder.typicode.com/todos/1").json()

    #st.write(data)

if __name__ == '__main__':
    main()

