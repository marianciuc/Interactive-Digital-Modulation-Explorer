import numpy as np
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import utils.utilities
from components.graphs import create_graph
from modulation import modulate_signal, demodulate_signal
from utils import ascii_to_binary_stream, binary_stream_to_ascii, calculate_ber, encode_hamming_7_4, decode_hamming_7_4, \
    noise


def register_callbacks(app):
    @app.callback(
        Output('modulated-signal-graph', 'figure'),
        Output('transmitted-signal-graph', 'figure'),
        Output('demodulated-signal-graph', 'figure'),
        Output('comparison-container', 'children'),
        Output('table-container', 'children'),
        Output('table-container-params', 'children'),
        Input('w-input', 'value'),
        Input('fs-input', 'value'),
        Input('tb-input', 'value'),
        Input('modulation', 'value'),
        Input('text', 'value'),
        Input('tabs', 'value'),
        Input('alpha-slider', 'value'),
        Input('beta-slider', 'value'),
        Input('noise-type', 'value'),
        Input('order-type', 'value')
    )
    def update_signal(_w, _fs, _tb, modulation_type, text, tab, alpha, beta, noise_type, order):
        try:
            w = float(_w)
            fs = int(_fs)
            tb = float(_tb)
        except ValueError:
            empty_fig = create_graph('', [], [], '')
            return empty_fig, empty_fig, empty_fig, [], [], []

        bits = ascii_to_binary_stream(text)
        encoded_bits = encode_hamming_7_4(bits)
        num_bits = len(encoded_bits)

        tc = tb * num_bits
        fn = w * (1 / tb)
        N = int(fs * tc)
        samples_per_bit = N // num_bits
        N = samples_per_bit * num_bits
        t = np.linspace(0, tc, N, endpoint=False)
        fn1 = (w + 1) / tb
        fn2 = (w + 2) / tb
        ts = 1 / fs

        params_table_data = [{
            'W': w,
            'Fs': fs,
            "Modulation Type": modulation_type,
            'Alpha': alpha,
            'Beta': beta,
            'Tb': tb,
            'fn': fn,
            'fn1': fn1,
            'fn2': fn2,
            'ts': ts,
            'N': N,
            'Bit count': num_bits
        }]

        table_params = dash_table.DataTable(
            columns=[{'name': col, 'id': col} for col in params_table_data[0].keys()],
            data=params_table_data,
            style_table={'margin': '20px auto', 'width': '50%'},
            style_cell={'textAlign': 'left', 'fontFamily': 'Arial, sans-serif', 'padding': '10px'}
        )

        if tab == 'modulation':
            signal = modulate_signal(encoded_bits, modulation_type, fn, t, fn1, fn2)

            if order == '1':
                if noise_type == 'white':
                    noisy_signal = signal + alpha * noise.white_noise(t, 10)
                elif noise_type == 'gaussian':
                    noisy_signal = signal + alpha * noise.gaussian_noise(t, 0, alpha)
                noisy_signal *= np.exp(-beta * t)
            else:
                noisy_signal = signal * np.exp(-beta * t)
                noisy_signal += alpha * noise.white_noise(t, 10)

            modulated_fig = create_graph('Modulated Signal' + modulation_type, t, signal, 'Amplitude')
            transmitted_fig = create_graph('Transmitted Signal' + modulation_type, t, noisy_signal, 'Amplitude')

            demodulated_bits = demodulate_signal(noisy_signal, modulation_type, fn, samples_per_bit, ts, N, fn1, fn2)
            demodulated_bits = utils.utilities.convert_to_binary_stream(demodulated_bits, samples_per_bit)
            decoded_hamming, syndrome = decode_hamming_7_4(demodulated_bits)
            ber = calculate_ber(bits, decoded_hamming)

            demodulated_fig = create_graph('Demodulated Signal', np.arange(len(bits)), bits, name="Original bit stream",
                                           y_name="", x_name="Bits")
            demodulated_fig.add_trace(
                go.Scatter(x=np.arange(len(bits)), y=decoded_hamming, mode='lines', name='Transmission result'))

            table_data = [{
                'Number of transmitted bits': len(bits),
                'Decoded phrase': binary_stream_to_ascii(decoded_hamming),
                'Syndrome': syndrome,
                'BER': ber
            }]

            table = dash_table.DataTable(
                columns=[{'name': col, 'id': col} for col in table_data[0].keys()],
                data=table_data,
                style_table={'margin': '20px auto', 'width': '50%'},
                style_cell={'textAlign': 'left', 'fontFamily': 'Arial, sans-serif', 'padding': '10px'}
            )
            return modulated_fig, transmitted_fig, demodulated_fig, None, table, table_params
        else:
            comparison_content = []
            comparison_data = []

            for modulation in ['ASK', 'PSK', 'FSK']:
                signal = modulate_signal(encoded_bits, modulation, fn, t, fn1, fn2)

                if order == '1':
                    if noise_type == 'white':
                        noisy_signal = signal + alpha * noise.white_noise(t, 10)
                    elif noise_type == 'gaussian':
                        noisy_signal = signal + alpha * noise.gaussian_noise(t, 0, alpha)
                    noisy_signal *= np.exp(-beta * t)
                else:
                    noisy_signal = signal * np.exp(-beta * t)
                    noisy_signal += alpha * noise.white_noise(t, 10)

                demodulated_bits = demodulate_signal(noisy_signal, modulation, fn, samples_per_bit, ts, N, fn1, fn2)
                demodulated_bits = utils.utilities.convert_to_binary_stream(demodulated_bits, samples_per_bit)
                decoded_hamming, syndrome = decode_hamming_7_4(demodulated_bits)
                ber = calculate_ber(bits, decoded_hamming)

                comparison_data.append({
                    'Modulation': modulation,
                    'BER': ber,
                    'Decoded phrase': binary_stream_to_ascii(decoded_hamming)
                })

            comparison_table = dash_table.DataTable(
                columns=[{'name': 'Modulation', 'id': 'Modulation'},
                         {'name': 'BER', 'id': 'BER'},
                         {'name': 'Decoded phrase', 'id': 'Decoded phrase'}],
                data=comparison_data,
                style_table={'margin': '20px auto', 'width': '80%'},
                style_cell={'textAlign': 'left', 'fontFamily': 'Arial, sans-serif', 'padding': '10px'}
            )

            comparison_content.append(comparison_table)
            empty_fig = create_graph('', [], [], '')
            return empty_fig, empty_fig, empty_fig, comparison_content, None, table_params
