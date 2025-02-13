const fake_data = [
    [
        {
            'wav_path': '/workspace/audio_team/usr/cgy/1_projects/36.3_CosyVoiceTeam/output500/clone_lm_textByt5GTE-55w_line100/0913_101611_cn_ras/59-明星男1 50+.wav',
            'PER': 2.857142857142857,
            'WER': 5.263157894736842,
            'ref': 'REF: 嗯,这个颜色挺适合你的,穿上显得特别有精神。',
            'res': 'RES:嗯这个颜色挺适合你了穿上显得特别有精神',
            'uuid': '59-明星男1 50+'
        },
        {
            'wav_path': '/workspace/audio_team/usr/cgy/1_projects/36.3_CosyVoiceTeam/output500/llama-55w_seed_0/0914_090410/59-明星男1 50+.wav',
            'PER': 0.0,
            'WER': 0.0,
            'ref': 'REF: 嗯,这个颜色挺适合你的,穿上显得特别有精神。',
            'res': 'RES:嗯这个颜色挺适合你的穿上显得特别有精神',
            'uuid': '59-明星男1 50+'
        }],
    [
        {
            'wav_path': '/workspace/audio_team/usr/cgy/1_projects/36.3_CosyVoiceTeam/output500/clone_lm_textByt5GTE-55w_line100/0913_101611_cn_ras/39-男22.wav',
            'PER': 2.857142857142857,
            'WER': 5.263157894736842,
            'ref': 'REF: 嗯,这个颜色挺适合你的,穿上显得特别有精神。',
            'res': 'RES:啊这个颜色挺适合你的穿上显得特别有精神',
            'uuid': '39-男22'
        },
        {
            'wav_path': '/workspace/audio_team/usr/cgy/1_projects/36.3_CosyVoiceTeam/output500/llama-55w_seed_0/0914_090410/39-男22.wav',
            'PER': 0.0,
            'WER': 0.0,
            'ref': 'REF: 嗯,这个颜色挺适合你的,穿上显得特别有精神。',
            'res': 'RES:嗯这个颜色挺适合你的穿上显得特别有精神',
            'uuid': '39-男22'
        }],
    [{
        'wav_path': '/workspace/audio_team/usr/cgy/1_projects/36.3_CosyVoiceTeam/output500/clone_lm_textByt5GTE-55w_line100/0913_101611_cn_ras/87-男6 30+.wav',
        'PER': 1.3157894736842104,
        'WER': 2.380952380952381,
        'ref': 'REF: 作为一个人工智能助手,我没有忙碌或空闲的概念,因为我始终在这里,随时准备回答问题和提供帮助。',
        'res': 'RES:作为一个人工智能助手我没有忙碌或空闲的概念因我始终在这里随时准备回答问题和提供帮助',
        'uuid': '87-男6 30+'
    },
        {
            'wav_path': '/workspace/audio_team/usr/cgy/1_projects/36.3_CosyVoiceTeam/output500/llama-55w_seed_0/0914_090410/87-男6 30+.wav',
            'PER': 2.631578947368421,
            'WER': 4.761904761904762,
            'ref': 'REF: 作为一个人工智能助手,我没有忙碌或空闲的概念,因为我始终在这里,随时准备回答问题和提供帮助。',
            'res': 'RES:作为一个人工智能助手我没有忙碌和空闲的概念因我始终在这里随时准备回答问题和提供帮助',
            'uuid': '87-男6 30+'
        }]
]

export default {
    fake_data: fake_data
}