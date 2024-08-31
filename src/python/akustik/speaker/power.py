import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def max_sound_pressure(SPL_ref, P_max, P_ref=1):
    """Maximum sound pressure level (SPL dB)

    Parameters
    ----------
        SPL_ref (float) : Reference sensitivity of the speaker driver
        P_max (float) : Maximum power the speaker can handle
        P_ref (float) : Power used for sensitivity measurement

    Returns
    ----------
        SPL_max (float) : Sound pressure level at P_max
    """
    SPL_max = SPL_ref + 10*np.log10(P_max/P_ref)
    return SPL_max


def power_for_target_spl(SPL_target, SPL_ref,  P_ref=1):
    """Required power for given max SPL
    """
    return P_ref * 10**((SPL_target-SPL_ref)/10)


def driver_spl_report(df, drivers, SPL_target=108):
    from akustik.plot.style import default_styles
    plt.rcParams.update(default_styles)
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    plt.title("Power Requirements")
    plt.xlabel("SPL [dB]")
    plt.ylabel("Power [W]")
    plt.grid(which="minor", color='#222222', linestyle=':', linewidth=0.5)
    plt.vlines(SPL_target, 0, 600, linestyles="--",
               label=f"Target {SPL_target} dB")

    for name, color in zip(drivers, colors):
        driver = df[df["Name"] == name]
        D_nominal = float(driver["D_nominal"].iloc[0])
        V_ref = float(driver["V_ref"].iloc[0])
        Z_ref = float(driver["Z_ref"].iloc[0])
        P_rms = float(driver["P_rms"].iloc[0])
        P_max = float(driver["P_max"].iloc[0])
        SPL_ref = float(driver["SPL_ref"].iloc[0])

        P_ref = (V_ref**2)/Z_ref
        SPL_rms = max_sound_pressure(SPL_ref, P_rms, P_ref)
        SPL_peak = max_sound_pressure(SPL_ref, P_max, P_ref)
        P_target = power_for_target_spl(SPL_target, SPL_ref, P_ref)

        print(f"- {name}:")
        print(f"    {Z_ref=:.2f} Ohm")
        print(f"    {P_ref=:.2f} W")
        print(f"    {P_rms=:.2f} W")
        print(f"    {P_max=:.2f} W")
        print(f"    {P_target=:.2f} W")
        print(f"    {SPL_ref=:.2f} dB")
        print(f"    {SPL_rms=:.2f} dB")
        print(f"    {SPL_peak=:.2f} dB")
        print("")

        SPL_desired = np.linspace(SPL_ref, SPL_peak, 1024)
        P_required = power_for_target_spl(SPL_desired, SPL_ref, P_ref)

        label = f"{name} {int(np.nan_to_num(D_nominal))}\" {P_target:.1f} W"
        plt.plot(SPL_desired[SPL_desired < SPL_rms],
                 P_required[SPL_desired < SPL_rms], label=label, color=color)
        plt.plot(SPL_desired[SPL_desired >= SPL_rms],
                 P_required[SPL_desired >= SPL_rms], linestyle="--", color=color)
        plt.scatter(SPL_rms, P_rms, color=color)

    plt.legend()
    plt.show()


def main(driver_db, SPL_target):
    df = pd.read_csv(driver_db)
    drivers = [
        # "Alcone AC 15",
        # "Alcone AC 8 HE",
        # "AMT U60W1.1-C",
        # "AMT U160W1.1-R",
        # "Dayton Audio AMTHR-4",
        # "Dayton Audio AMTPRO-4",
        # "Morel CAT 328-110",
        # "Morel EM 1308",
        # "Morel ET 338",
        # "Morel ET 448",
        # "Morel ST 1048",
        # "Mundorf AMT25CS2.1-R",
        # "Mundorf AMT29CM1.1-R",
        # "JBL Selenium D220Ti-8",
        # "Dayton Audio RSS265HF-8",
        # "Dayton Audio RSS315HFA-8",
        # "Dayton Audio RSS315HF-4",
        # "Dayton Audio RSS315HO-4",
        "Dayton Audio RSS390HF-4",
        "Dayton Audio RSS390HO-4",
        "Dayton Audio RSS460HO-4",
        # "Radian 950NeoPB-8",
        # "ScanSpeak Discovery 15M/4624G00",
        # "ScanSpeak Discovery 30W/4558T00",
        # "ScanSpeak Revelator 32W/4878T00",
        # "ScanSpeak Revelator 32W/4878T01",
        # "Supravox 285 GMF",
        # "Supravox 400 GMF",
        # "Supravox 400-2000 EXC",
        # "TAD TD-2002",
        "TAD TL-1601b",
        "TAD TL-1801",
        # "Volt Loudspeakers VM527",
        # "Volt Loudspeakers VM752",
        # "Volt Loudspeakers RV2501",
        # "Volt Loudspeakers RV3143",
        # "Volt Loudspeakers RV3863",
        # "Volt Loudspeakers RV4564",
    ]
    driver_spl_report(df, drivers, SPL_target=SPL_target)
