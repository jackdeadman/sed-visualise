from yaafelib import *


if __name__ == '__main__':
    audiofile = 'test.wav'
    # Build a DataFlow object using FeaturePlan
    fp = FeaturePlan(sample_rate=44100)
    fp.addFeature('mfcc: MFCC blockSize=512 stepSize=256')
    df = fp.getDataFlow()
    # or load a DataFlow from dataflow file.
    # df = DataFlow()
    # df.load(dataflow_file)
    # configure an Engine
    engine = Engine()
    engine.load(df)
    # extract features from an audio file using AudioFileProcessor
    afp = AudioFileProcessor()
    afp.processFile(engine,audiofile)
    feats = engine.readAllOutputs()
    # and play with your features
    # extract features from an audio file and write results to csv files
    afp.setOutputFormat('csv','output',{'Precision':'8'})
    afp.processFile(engine,audiofile)
    # this creates output/myaudio.wav.mfcc.csv,
    #              output/myaudio.wav.mfcc_d1.csv and
    #              output/myaudio.wav.mfcc_d2.csv files.
    #
    #
    # extract features from a numpy array
    # import numpy
    # audio = numpy.random.randn(1,100000)
    # feats = engine.processAudio(audio)
