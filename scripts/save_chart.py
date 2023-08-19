import datetime
import os

def save_chart(plt, chart_name):
    target_dir = '../generated_plots/'

    today = datetime.datetime.now()
    formatted_date = today.strftime('%Y%m%d_%H%M')

    target_dir += formatted_date + '/'

    # Make a directory if it does not exist yet
    os.makedirs(target_dir, exist_ok=True)

    # Get today's date
    plt.savefig(target_dir + chart_name + '.png', dpi=300, transparent=False, bbox_inches='tight')

    # Close the plot
    plt.close()