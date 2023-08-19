import datetime
import os
import inspect

def save_chart(plt, chart_name):
    target_dir = '../generated_plots/'

    today = datetime.datetime.now()
    formatted_date = today.strftime('%Y%m%d_%H%M')

    target_dir += formatted_date + '/'

    # Make a directory if it does not exist yet
    os.makedirs(target_dir, exist_ok=True)

    # Get today's date
    file_path = target_dir + chart_name + '.png'
    plt.savefig(file_path, dpi=200, transparent=False, bbox_inches='tight')

    print("saved " + file_path)

    # Close the plot
    plt.close()

def display_or_save(plt, save_to_file_flag):
    if save_to_file_flag:
        # Get the caller's file name
        caller_filename = inspect.stack()[1].filename
        current_file = os.path.basename(caller_filename)
        stripped_current_file = os.path.splitext(current_file)[0]
        save_chart(plt, stripped_current_file)
    else:
        plt.show()