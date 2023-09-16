
import whispercpp as w
import typing as t
import sys


def main(**kwargs: t.Any):
    iterator: t.Iterator[str] | None = None
    try:
        iterator = w.Whisper.from_pretrained(
            model_name='../models/ggml-small.bin'
        ).stream_transcribe(**kwargs)
    finally:
        assert iterator is not None, "Something went wrong!"
        sys.stderr.writelines(
            ["\nTranscription (line by line):\n"] + [f"{it}\n" for it in iterator]
        )
        sys.stderr.flush()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--device_id", type=int, help="Choose the audio device", default=1
    )
    parser.add_argument(
        "--length_ms",
        type=int,
        help="Length of the audio buffer in milliseconds",
        default=5000,
    )
    parser.add_argument(
        "--sample_rate",
        type=int,
        help="Sample rate of the audio device",
        default=w.api.SAMPLE_RATE,
    )
    parser.add_argument(
        "--n_threads",
        type=int,
        help="Number of threads to use for decoding",
        default=8,
    )
    parser.add_argument(
        "--step_ms",
        type=int,
        help="Step size of the audio buffer in milliseconds",
        default=4000,
    )
    parser.add_argument(
        "--keep_ms",
        type=int,
        help="Length of the audio buffer to keep in milliseconds",
        default=200,
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        help="Maximum number of tokens to decode",
        default=100,
    )
    parser.add_argument(
        "--language",
        type=str,
        default='es',
    )
    parser.add_argument("--audio_ctx", type=int, help="Audio context", default=0)

    args = parser.parse_args()

    main(**vars(args))