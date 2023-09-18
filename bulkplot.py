"""
Program untuk membuat animasi plot menggunakan multiprocessing
"""
import os
import time
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl

from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

_start_time = time.time()

def logfunc(output):
    """
    Fungsi untuk mencetak log
    """
    i, filename = output
    text = f'Pada {time.time()-_start_time:7.2f} s'
    text = text + f': i = {i:>4d}'
    print(text)

def plot_animasi(t: int, plot_dir: str):
    """
    Fungsi untuk membuat plot animasi

    Parameter
    ---------
    t : int
        Indeks waktu
    plot_dir : str
        Direktori untuk menyimpan plot
    """

    fig = plt.figure(figsize=(5, 5), dpi=300)
    gs = GridSpec(
        2, 1, figure=fig,
        hspace=0.2,
        height_ratios=(2, 1)
    )

    gs_cont = GridSpecFromSubplotSpec(
        2, 1, subplot_spec=gs[0],
        hspace=0.05,
        height_ratios=(0.05, 1)
    )

    ax_cont = fig.add_subplot(gs_cont[1])
    ax_cbar = fig.add_subplot(gs_cont[0])
    ax_meas = fig.add_subplot(gs[1], sharex=ax_cont)

    ### Solusi ###
    # Plot kontur
    x = np.linspace(0., 500., nx)
    y = np.linspace(0., 100., ny)
    X, Y = np.meshgrid(x, y)
    bz_max = np.max(np.abs(bz))
    cont_plot = ax_cont.pcolormesh(
        X, Y, bz.T, vmin=-bz_max, vmax=bz_max, cmap='RdBu')
    cbar = fig.colorbar(cont_plot, cax=ax_cbar, orientation='horizontal')

    # Plot trajektori
    ax_cont.plot(x[x_par[:t]], y[y_par[:t]], 'k-')
    ax_cont.plot(x[x_par[t]], y[y_par[t]], 'mo')

    # Atur label
    ax_cont.set_ylabel(r'$y$')
    ax_cbar.set_xlabel(rf'$B_z (t = {t})$')

    ax_cbar.xaxis.set_label_position('top')
    ax_cbar.xaxis.set_ticks_position('top')

    # Plot medan Bz
    bz_traj = bz[x_par, y_par]
    ax_meas.plot(x[x_par], bz_traj, 'k-', alpha=0.5)
    ax_meas.plot(x[x_par[:t]], bz_traj[:t], 'k-')
    ax_meas.plot(x[x_par[t]], bz_traj[t], 'mo')

    # Atur label
    ax_meas.set_xlabel(r'$x$')
    ax_meas.set_ylabel(r'$B_z$')
    ### Solusi ###

    # Simpan gambar
    out_file = os.path.join(plot_dir, f'animasi_{t:03d}.png')
    fig.savefig(out_file)
    plt.close(fig)

    return t, 

if __name__ == "__main__":
    # Baca data medan Bz
    with open('bz.pkl', 'rb') as f:
        bz = pkl.load(f)

    # Particle Trajectory
    nx, ny = bz.shape
    x_par = np.arange(nx)
    y_par = ny/4 * (2 + np.sin(2*np.pi*x_par/nx))
    y_par = y_par.round().astype(int)

    nt = nx
    plot_dir = 'animasi'

    os.makedirs(plot_dir, exist_ok=True)

    # Mulai Pool
    n_pool = 4
    with mp.Pool(4) as pool:
        for i in range(nt):
            pool.apply_async(plot_animasi_mp, args=(...), callback=logfunc)

        pool.close()
        pool.join()
    
    # Print waktu total
    end_time = time.time()
    print(f'== Total waktu: {end_time - _start_time:.2f} s')