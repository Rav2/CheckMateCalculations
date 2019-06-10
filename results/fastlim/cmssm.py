import copy

class Point:
	def __init__(self, m0, mhalf, tanB, A0, sign):
		self.m0 = m0
		self.mhalf = mhalf
		self.tanB = tanB
		self.A0 = A0
		self.sign = sign
		self.top_group = None
		self.disc_top_group = None
		self.procs = []
		self.errors = []
		self.allowed_procs = []
		self.discarded_procs = []
		self.maxrate = None
		self.maxxsec = None
		self.maxproc = None
		self.disc_maxrate = None
		self.disc_maxxsec = None
		self.disc_maxproc = None
		self.tot_allowed_xsec = None
		self.tot_allowed_rate = None
		self.tot_disc_xsec = None
		self.tot_disc_rate = None
		self.top3proc = []
		self.broken = False
		self.mass_spectrum = None
		self.name = "{m0}_{mhalf}_{tanB}_{A0}_{sign}".format(m0=self.m0, mhalf=self.mhalf, tanB=self.tanB, A0=self.A0, sign=self.sign)
		self.limited_to_group = False

	def add_data(self, proc, xsec, rate):
		self.procs.append(Process(proc.strip(), xsec, rate, False))

	def set_tops(self):
		if len(self.procs) == 0:
			self.maxxsec = 0.0
			self.maxrate = 0.0
			self.maxproc = 'no_data'
			self.disc_maxxsec = 0.0
			self.disc_maxrate = 0.0
			self.tot_allowed_xsec = 10.0**-20
			self.tot_allowed_rate = 10.0**-20
			self.tot_disc_xsec =10.0**-20
			self.tot_disc_rate = 10.0**-20
			self.top_group = 'no_data'
			self.disc_top_group = 'no_data'
			return

		if len(self.allowed_procs) == 0:
			print('[WARNING] No allowed procs for {}_{}_{}_{}_{}'.format(self.m0, self.mhalf, self.tanB, self.A0, self.sign) + ' ; ' + \
			'Tot no of procs: {}, allowed: {}, discarded: {}, diff: {}'.format(len(self.procs), len(self.allowed_procs), len(self.discarded_procs), \
			                                                                   len(self.procs) - len(self.allowed_procs) - len(self.discarded_procs)))
			self.maxrate = 0.0
			self.maxxsec = 0.0
			self.maxproc = 'no_data'
			self.tot_allowed_xsec = 10.0**-20
			self.tot_allowed_rate = 10.0**-20
			self.top_group = 'no_data'
		else:
			self.allowed_procs.sort(key=lambda x: x.rate, reverse=True)
			self.maxproc = self.allowed_procs[0].proc
			self.maxrate = self.allowed_procs[0].rate
			self.maxxsec = self.allowed_procs[0].xsec
			self.top_group = self.allowed_procs[0].group
			for ii in range(0, min(3, len(self.allowed_procs))):
				self.top3proc.append(self.allowed_procs[ii].proc)

		# do the same for discarded processes
		if len(self.discarded_procs) > 0:
			self.discarded_procs.sort(key=lambda x: x.rate, reverse=True)
			self.disc_maxproc = self.discarded_procs[0].proc
			self.disc_maxrate = self.discarded_procs[0].rate
			self.disc_maxxsec = self.discarded_procs[0].xsec
			self.disc_top_group = self.discarded_procs[0].group
		else:
			self.disc_maxproc = 'no_data'
			self.disc_maxrate = 0.0
			self.disc_maxxsec = 0.0
			self.tot_disc_xsec = 10.0 ** -20
			self.tot_disc_rate = 10.0**-20
			self.disc_top_group = 'no_data'


	def set_allowed(self, topo):
		allowed = {}
		# extract topologies that are allowed
		topo_copy = copy.deepcopy(topo)
		for proc in topo_copy:
			proc.analyze_process(self.mass_spectrum)
			if proc.allowed:
				allowed[proc.proc] = proc.brackets
		# get indices of processes in self.proc that should be allowed
		indices = [ii for ii, proc in enumerate(self.procs) if proc.proc in allowed.keys()]
		for ii in indices:
			self.procs[ii].brackets = allowed[self.procs[ii].proc]
			self.procs[ii].analyze_process(self.mass_spectrum)
			if self.procs[ii].allowed:
				self.allowed_procs.append(self.procs[ii])
			else:
				self.discarded_procs.append(self.procs[ii])
		self.tot_allowed_xsec = sum([a.xsec for a in self.allowed_procs])
		self.tot_allowed_rate = sum([a.rate for a in self.allowed_procs])

		# do the same for discarded processes
		indices = [ii for ii, proc in enumerate(self.procs) if proc.proc not in allowed.keys()]
		for ii in indices:
			# it doesnt need to be False, but as long as they are discarded, it doesnt matter but something needs to be set
			self.procs[ii].brackets = False
			self.procs[ii].analyze_process(self.mass_spectrum)
			self.discarded_procs.append(self.procs[ii])
		# self.allowed_procs[-1].analyze_process(self.mass_spectrum)
		self.tot_disc_xsec = sum([a.xsec for a in self.discarded_procs])
		self.tot_disc_rate = sum([a.rate for a in self.discarded_procs])
		# if  len(self.procs) - len(self.allowed_procs) - len(self.discarded_procs) != 0:
		# 	print('Tot no of procs: {}, allowed: {}, discarded: {}, diff: {}'.format(len(self.procs), len(self.allowed_procs), len(self.discarded_procs), \
		#                                                                          len(self.procs) - len(self.allowed_procs) - len(self.discarded_procs)))

	def add_err(self, msg):
		self.errors.append(msg)

	def get_proc_no(self):
		return len(self.procs)

	def is_broken(self):
		self.broken = True

	def limit_to_group(self, group, topo):
		self.limited_to_group = True
		self.allowed_procs = []
		self.discarded_procs = []
		self.maxrate = None
		self.maxxsec = None
		self.maxproc = None
		self.disc_maxrate = None
		self.disc_maxxsec = None
		self.disc_maxproc = None
		self.disc_top_group = None
		self.top3proc = []
		self.tot_disc_xsec = None
		self.tot_disc_rate = None
		self.tot_allowed_xsec = None
		self.tot_allowed_rate = None
		self.tot_allowed_xsec = 10.0**-20
		self.tot_allowed_rate = 10.0**-20
		self.top_group = None
		processes = [p for p in self.procs if p.group == group]
		self.procs = processes
		if len(self.procs) > 0:
			self.set_allowed(topo)
			self.set_tops()
		else:
			self.top_group = 'no_data'


class Process():
	def __init__(self, proc, xsec, rate, brackets=False):
		self.proc = proc
		self.xsec = xsec
		self.rate = rate
		self.init_pars = None
		self.SM_pars = None
		self.SUSY_pars = None
		self.brackets = brackets
		self.allowed = False
		self.group = None

	def detectGroup(self):
		if self.SM_pars is None:
			raise Exception('First anlyze the processes, then detect group!')
		else:
			try:
				if self.init_pars[0] == self.init_pars[1]:
					if self.init_pars[0] == 'G':
						if len(self.SUSY_pars[0]) >=1 and len(self.SUSY_pars[1]) >= 1 and self.SUSY_pars[0][0] in ('T1', 'T2', 'B1', 'B2') and self.SUSY_pars[1][0] in ('T1', 'T2', 'B1', 'B2'):
							self.group = 'G(G->stop)'
						elif len(self.SUSY_pars[0]+self.SUSY_pars[1]) == 0 and all([x in ('b','t','q') for x in self.SM_pars]):
							self.group = 'G(G->quark)'
						elif len(self.SUSY_pars[0]+self.SUSY_pars[1]) == 0 and self.SM_pars.count('g') == 1:
							self.group = 'G(G->g)'
						else:
							self.group = 'G(G->other)'
					elif self.init_pars[0] in ('T1', 'T2', 'B1', 'B2'):
						if len(self.SUSY_pars[0] + self.SUSY_pars[1]) == 0:
							self.group = 'T(T->N1)'
						else:
							self.group = 'T(T->other)'
					elif self.init_pars[0] == 'Q':
						if len(self.SUSY_pars[0] + self.SUSY_pars[1]) == 0:
							self.group = 'Q(Q->N1)'
						elif len(self.SUSY_pars[0]) == len(self.SUSY_pars[1]) and len(self.SUSY_pars[1]) == 1 and \
										self.SUSY_pars[0][0][0] in ('N', 'C') and self.SUSY_pars[1][0][0] in ('N', 'C'):
							self.group = 'Q(Q->X)'
						else:
							self.group = 'Q(Q->other)'
					elif self.init_pars[0] in ('E', 'M', 'TAU1', 'TAU2', 'NU', 'NUT'):
						if len(self.SUSY_pars[0] + self.SUSY_pars[1]) == 0:
							self.group = 'SL(SL->N1)'
						else:
							self.group = 'SL(SL->other)'
					elif self.init_pars[0][0] in ('C', 'N'):
						if len(self.SUSY_pars[0] + self.SUSY_pars[1]) == 0:
							self.group = 'X(X->N1)'
						elif len(self.SUSY_pars[0]) == len(self.SUSY_pars[1]) and len(self.SUSY_pars[1]) == 1 and \
										self.SUSY_pars[0][0] in ('E', 'M', 'TAU1', 'TAU2', 'NU', 'NUT') and \
										self.SUSY_pars[1][0] in ('E', 'M', 'TAU1', 'TAU2', 'NU', 'NUT'):
							self.group = 'X(X->SL)'
						else:
							self.group = 'X(X->other)'
					else:
						self.group = 'other'
				else:
					if self.init_pars[0][0] in ('C', 'N') and self.init_pars[1][0] in ('C', 'N'):
						if len(self.SUSY_pars[0] + self.SUSY_pars[1]) == 0:
							self.group = 'X(X->N1)'
						elif len(self.SUSY_pars[0]) == len(self.SUSY_pars[1]) and len(self.SUSY_pars[1]) == 1 and \
										self.SUSY_pars[0][0] in ('E', 'M', 'TAU1', 'TAU2', 'NU', 'NUT') and \
										self.SUSY_pars[1][0] in ('E', 'M', 'TAU1', 'TAU2', 'NU', 'NUT'):
							self.group = 'X(X->SL)'
						else:
							self.group = 'X(X->other)'
					else:
						self.group = 'other'
			except Exception as e:
				print(e)


	def analyze_process(self, masses, omit_mass_check=False):
		SM1 = ('q', 'e', 'b', 't', 'g', 'z', 'h', 'w', 'n', 'm')
		SM2 = ('ta', 'nu')
		SM = SM1+SM2
		SUSY1 = ('G', 'Q', 'E', 'M')
		SUSY2 = ('N1', 'N2', 'N3', 'N4', 'T1', 'T2', 'B1', 'B2', 'C1', 'C2', 'NU')
		SUSY3 = ('NUT')
		SUSY4 = ('TAU1', 'TAU2')
		SUSY = SUSY1 + SUSY2 + SUSY4

		br1 = self.proc.split('_')[0]
		br2 = self.proc.split('_')[1]
		sm_pars = []
		susy_pars = []
		# extract particles from the string
		for br in (br1, br2):
			susys = []
			for ii, char in enumerate(br):
				if ii >= len(br):
					break

				if char.isupper():
					if len(br[ii:])>3 and br[ii:ii+4] in SUSY:
						susys.append(br[ii:ii+4])
						ii = ii+4
					elif len(br[ii:])>2 and br[ii:ii+3] in SUSY:
						susys.append(br[ii:ii+3])
						ii = ii+3
					elif len(br[ii:])>1 and br[ii:ii+2] in SUSY:
						susys.append(br[ii:ii+2])
						ii = ii+2
					elif char in SUSY:
						susys.append(char)
				else:
					if len(br[ii:])>1 and br[ii:ii+2] in SM:
						sm_pars.append(br[ii:ii+2])
						ii = ii+2
					elif char in SM:
						sm_pars.append(char)
			susy_pars.append(susys)
		# write found particles to fields
		self.init_pars = (susy_pars[0][0], susy_pars[1][0])
		self.SM_pars = tuple(sm_pars)
		self.SUSY_pars = (susy_pars[0][1:-1], susy_pars[1][1:-1])
		tot_no_of_SUSY_pars = len(set(susy_pars[0] + susy_pars[1]))
		# parse brackets == check for masses
		if self.brackets and len(self.SUSY_pars[0]) == len(self.SUSY_pars[1]) and not omit_mass_check:
			ew_pars =  ('C1', 'C2', 'N1', 'N2', 'N3', 'N4')
			stops = ('T1', 'T2', 'B1', 'B2')

			for p1, p2 in zip(susy_pars[0][0:-1], susy_pars[1][0:-1]):
				m1 = masses[p1]
				m2 = masses[p2]
				if p1 != p2 and ((p1 in ew_pars and p2 in ew_pars) or (p1 in stops and p2 in stops)) and abs(m1-m2)/min((m1, m2)) < 0.1:
					tot_no_of_SUSY_pars -= 1
		# set topological groups
		self.detectGroup()
		# we discard processes that require more than 3 SUSY masses
		if tot_no_of_SUSY_pars < 4:
			self.allowed = True
		else:
			self.allowed = False
