import os, subprocess

class Benchmark:
	def __init__(self, name, location, program, options):
		self.name = name
		self.location = location
		self.program = program
		self.options = options

num_inst = 10000000
predictors = ['BiModeBP', 'TAGE', 'PerceptronBasicBP', 'PerceptronHashedBP']
benchmarks = []
benchmarks.append(Benchmark('500.perlbench_r',
	'/root/spec2017/benchspec/CPU/500.perlbench_r/run/run_base_test_perceptron-m64.0000',
	'perlbench_r_base.perceptron-m64',
	'-I. -I./lib test.pl'))
benchmarks.append(Benchmark('520.omnetpp_r',
        '/root/spec2017/benchspec/CPU/520.omnetpp_r/run/run_base_test_perceptron-m64.0000',
	'omnetpp_r_base.perceptron-m64',
        '-c General -r 0'))
benchmarks.append(Benchmark('523.xalancbmk_r',
        '/root/spec2017/benchspec/CPU/523.xalancbmk_r/run/run_base_test_perceptron-m64.0000',
	'cpuxalan_r_base.perceptron-m64',
        '-v test.xml xalanc.xsl'))
benchmarks.append(Benchmark('525.x264_r',
        '/root/spec2017/benchspec/CPU/525.x264_r/run/run_base_test_perceptron-m64.0000',
	'x264_r_base.perceptron-m64',
        '--dumpyuv 50 --frames 156 -o BuckBunny_New.264 BuckBunny.yuv 1280x720'))
benchmarks.append(Benchmark('531.deepsjeng_r',
        '/root/spec2017/benchspec/CPU/531.deepsjeng_r/run/run_base_test_perceptron-m64.0000',
	'deepsjeng_r_base.perceptron-m64',
        'test.txt'))
benchmarks.append(Benchmark('541.leela_r',
        '/root/spec2017/benchspec/CPU/541.leela_r/run/run_base_test_perceptron-m64.0000',
	'leela_r_base.perceptron-m64',
        'test.sgf'))
benchmarks.append(Benchmark('548.exchange2_r',
        '/root/spec2017/benchspec/CPU/548.exchange2_r/run/run_base_test_perceptron-m64.0000',
        'exchange2_r_base.perceptron-m64',
        '0'))
benchmarks.append(Benchmark('557.xz_r',
        '/root/spec2017/benchspec/CPU/557.xz_r/run/run_base_test_perceptron-m64.0000',
        'xz_r_base.perceptron-m64',
        'cpu2006docs.tar.xz 4 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 1548636 1555348 0'))

def run_variant(cpu, freq, l2, variant):
	for prog_name, prog_loc in benchmarks.items():
		inst = "gem5/build/X86/gem5.opt --outdir=CS251A-Proj1/%s_%s gem5/configs/example/se.py --cmd=%s --cpu-type=%s --l1d_size=64kB --l1i_size=64kB --caches %s --cpu-clock=%s --mem-type=DDR3_1600_8x8" % (prog_name, variant, prog_loc, cpu, l2, freq)
		subprocess.run(inst.split())

def run_test(predictor, bench):
	inst1 = '/root/gem5/build/X86/gem5.opt --outdir=/root/CS251A_final_output/{pred}-{bench} /root/gem5/configs/example/se.py --cmd={cmd}'\
			.format(pred=predictor, bench=bench.name, cmd=bench.program)
	inst2 =	(' --options=\"{opt}\" --bp-type={pred}').format(opt=bench.options, pred=predictor)
	inst3 =	' --cpu-type=DerivO3CPU --caches --l2cache --l1d_size=64kB --l1i_size=64kB --l2_size=512kB --mem-size=8GB'
	inst4 =	' --fast-forward=1000000 --maxinsts=%d' % (num_inst)
	inst = inst1 + inst2 + inst3 + inst4
	task = subprocess.Popen(inst, cwd=bench.location, shell=True)
	task.wait()

for pred in predictors:
	for bench in benchmarks:
		run_test(pred, bench)
print ("DONE WITH EVERYTHING")

