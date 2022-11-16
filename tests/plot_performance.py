import matplotlib
from matplotlib import pyplot as plt

plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=17)
plt.rc('axes', titlesize=21)
plt.rc('legend', fontsize=15)
plt.rc('ytick', labelsize=17)
plt.rc('axes', labelsize=17)
plt.rc('lines', linewidth=2, markersize=8, markeredgecolor='black')

dataset_name = 'BPIC 2020'  # Sepsis, BPIC 2020

if dataset_name == 'Sepsis':
    model_checking_data_len = [17, 34, 51, 69]
    model_checking_data_d4py = [0.2324790954589843, 2.3160719871520996, 2.7095189094543457, 3.0642449855804443]
    model_checking_data_rum = [0.527, 2.583, 3.573, 4.040]

    discovery_no_data_len = [0.2, 0.4, 0.6, 0.8]
    discovery_no_data_d4py = [32.231475830078125, 28.104568004608154, 26.241751194000244, 11.41601300239563]

    query_1_nodata_d4py = [0.24416518211364746, 0.1822190284729004, 0.12294220924377441, 0.059205055236816406]
    query_2_nodata_d4py = [2.171064853668213, 1.6007418632507324, 1.0806610584259033, 0.5427911281585693]
else:
    model_checking_data_len = [17, 34, 51, 68]
    model_checking_data_d4py = [4.410614013671875, 13.101680278778076, 21.83715295791626, 29.120752811431885]
    model_checking_data_rum = [17.521, 23.818, 35.946, 93.340]

    discovery_no_data_len = [0.2, 0.4, 0.6, 0.8]
    discovery_no_data_d4py = [186.79399704933167, 120.53131103515625, 121.06814503669739, 72.35855984687805]

    query_1_nodata_d4py = [1.7119998931884766, 1.3102271556854248, 0.8156023025512695, 0.29633212089538574]
    query_2_nodata_d4py = [49.54182815551758, 37.321816205978394, 24.311094999313354, 10.868824005126953]

fig = plt.figure()
plt.plot(model_checking_data_len, model_checking_data_rum, ls='-.', c='forestgreen', label="RuM", marker='>')
plt.plot(model_checking_data_len, model_checking_data_d4py, ls='-', c='mediumorchid', label="Declare4Py", marker='D')
plt.legend()
plt.title(f"Conformance checking - {dataset_name} log")
plt.xlabel("Number of model constraints")
plt.ylabel("Time [s]")
plt.tight_layout()
fig.savefig(f"conformance_checking_{dataset_name}.pdf")
fig.clear()

plt.plot(discovery_no_data_len, discovery_no_data_d4py, ls='-', c='mediumorchid', label="Declare4Py", marker='D')
plt.title(f"Model discovery - {dataset_name} log")
plt.xlabel("Itemset support")
plt.ylabel("Time [s]")
plt.tight_layout()
fig.savefig(f"model_discovery_{dataset_name}.pdf")
fig.clear()

plt.plot(discovery_no_data_len, query_1_nodata_d4py, ls='-', c='mediumorchid',  label="1 variable", marker='D')
plt.plot(discovery_no_data_len, query_2_nodata_d4py, ls=':', c='darkorchid',  label="2 variables", marker='^')
plt.legend(loc="upper left")

plt.title(f"Query checking - {dataset_name} log")
plt.xlabel("Declare constraint support")
plt.ylabel("Time [s]")
plt.tight_layout()
fig.savefig(f"query_checking_{dataset_name}.pdf")
