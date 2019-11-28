'''
Module used to implement querys to verify audio features
'''
import numpy
import graphene
import accounts.utility as Utility

class AudioQuery(graphene.AbstractType):
    '''
    Class used to implement querys to verify audio features
    '''
    audio_has_good_volume = graphene.Boolean(
        audio_data=graphene.List(graphene.Float, required=True),
        audio_samplerate=graphene.Int(required=True)
    )

    def resolve_audio_has_good_volume(self, info, **kwargs):
        '''
        Find out if the audio has a good volume
        '''
        audio_data = kwargs.get('audio_data')
        audio_samplerate = kwargs.get('audio_samplerate')
        audio_data = Utility.treat_audio_data(audio_data, audio_samplerate)

        return len(audio_data) / audio_samplerate > 0.3
