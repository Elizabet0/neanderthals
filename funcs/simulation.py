import msprime
import sys
sys.path.append('..')
from parameters import params, Ne, t, t_second_wave

def simulate_one_pulse(seed,admixture_prop=0.1):
    demography=msprime.Demography()
    for name,size in [("AF",Ne['af']),("EU",Ne['eu']),("AMH",Ne['amh']),
                      ("ND",Ne['nd']),("ANCES",Ne['anc']),("OOA",Ne['ooa'])]:
        demography.add_population(name=name, initial_size=size)

    demography.add_population_parameters_change(time=0, initial_size=Ne['eu'], population="EU", growth_rate=0.00202)
    demography.add_population_parameters_change(time=t['t_eu_growth'], initial_size=Ne['eu_growth'],population="EU",growth_rate=0)
    demography.add_admixture(
        time=t['t_nd_migration'],
        derived="EU",
        ancestral=["OOA","ND"],
        proportions=[1-admixture_prop, admixture_prop]
    )
    demography.add_population_split(
        time=t['t_ooa'],
        derived=["AF","OOA"],
        ancestral="AMH"
    )
    demography.add_population_split(
        time=t['t_amh'],
        derived=["AMH","ND"],
        ancestral="ANCES"
    )
    demography.sort_events()
    ts=msprime.sim_ancestry(
        samples=[
            msprime.SampleSet(params['n_eu'],ploidy=params['ploidy'],population='EU'),
            msprime.SampleSet(params['n_af'],ploidy=params['ploidy'],population='AF'),
            msprime.SampleSet(params['n_nd'],ploidy=params['ploidy'],population='ND',time=t['t_nd_samples'])
        ],
        ploidy=params['ploidy'],
        sequence_length=params['chrom_length'],
        recombination_rate=params['recomb_rate'],
        demography=demography,
        random_seed=seed,
        record_migrations=True
    )
    return ts


def simulate_two_pulses(seed, prop_first=0.05, prop_second=0.05):
    demography = msprime.Demography()
    for name,size in [("AF",Ne['af']),("EU",Ne['eu']),("AMH",Ne['amh']),
                         ("ND",Ne['nd']),("ANCES",Ne['anc']),("OOA",Ne['ooa'])]:
        demography.add_population(name=name,initial_size=size)
    demography.add_population_parameters_change(time=0,initial_size=Ne['eu'],population="EU",growth_rate=0.00202)
    demography.add_population_parameters_change(time=t['t_eu_growth'],initial_size=Ne['eu_growth'],population="EU",growth_rate=0)
    demography.add_admixture(
        time=t['t_nd_migration'],
        derived="EU",
        ancestral=["OOA","ND"],
        proportions=[1-prop_first,prop_first]
    )
    demography.add_mass_migration(
        time=t_second_wave,
        source="EU",
        dest="ND",
        proportion=prop_second
    )
    demography.add_population_split(
        time=t['t_ooa'],
        derived=["AF","OOA"],
        ancestral="AMH"
    )
    demography.add_population_split(
        time=t['t_amh'],
        derived=["AMH","ND"],
        ancestral="ANCES"
    )
    demography.sort_events()
    ts=msprime.sim_ancestry(
        samples=[
            msprime.SampleSet(params['n_eu'],ploidy=params['ploidy'],population='EU'),
            msprime.SampleSet(params['n_af'], ploidy=params['ploidy'],population='AF'),
            msprime.SampleSet(params['n_nd'],ploidy=params['ploidy'],population='ND',time=t['t_nd_samples'])
        ],
        ploidy=params['ploidy'],
        sequence_length=params['chrom_length'],
        recombination_rate=params['recomb_rate'],
        demography=demography,
        random_seed=seed,
        record_migrations=True
    )
    return ts

