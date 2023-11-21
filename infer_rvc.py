import os
from scipy.io import wavfile
import infer_batch_rvc
from infer_batch_rvc import get_vc, vc_single


def infer_rvc(
    f0up_key,
    input_path,
    index_path,
    f0method,
    opt_path,
    model_path,
    index_rate,
    crepe_hop_length
):
    get_vc(model_path)
    wav_opt = vc_single(0, input_path, f0up_key, None, f0method, index_path, index_rate, crepe_hop_length)
    out_path = os.path.join(opt_path, f"{os.path.basename(input_path)}_converted.wav")
    wavfile.write(out_path, infer_batch_rvc.tgt_sr, wav_opt)
    return out_path


def run_rvc(
    f0up_key: str,
    original_audio_path: str,
    index_path: str,
    f0method: str,
    model_path: str,
    index_rate: float,
    device: str,
    is_half: bool,
    filter_radius: int,
    resample_sr: int,
    rms_mix_rate: float,
    protect: float,
    hop_length: int,
    output_path: str
):
    infer_batch_rvc.set_params_temp(
        _device=device,
        _is_half=is_half,
        _filter_radius=filter_radius,
        _resample_sr=resample_sr,
        _rms_mix_rate=rms_mix_rate,
        _protect=protect,
    )

    from infer_batch_rvc import config

    if device == "cpu":  # Workaround for "slow_conv2d_cpu" not implemented for 'Half'
        config.is_half = is_half

    # if infer_batch_rvc.hubert_model is None:
    #     get_and_load_hubert()

    return infer_rvc(
        f0method=f0method,
        f0up_key=f0up_key,
        input_path=original_audio_path,
        index_path=index_path,
        index_rate=index_rate,
        model_path=model_path,
        opt_path=output_path,
        crepe_hop_length=hop_length
    )