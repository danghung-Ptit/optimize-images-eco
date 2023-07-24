from optimize_images.data_structures import TaskResult, Task, OutputConfiguration
from optimize_images.do_optimization import do_optimization



def optimize_as_batch(src_path, watch_dir=False, recursive=True, quality=80, remove_transparency=False,
                      reduce_colors=False, max_colors=256, max_w=0, max_h=0, keep_exif=False,
                      convert_all=False, conv_big=False, force_del=False, bg_color=(255, 255, 255),
                      grayscale=False, ignore_size_comparison=False, fast_mode=False, jobs=0, output_config = None):
    """ Try to reduce the file size of all images found in the specified path,
        using The specified parameters.

    :param src_path:
    :param watch_dir:
    :param recursive:
    :param quality:
    :param remove_transparency:
    :param reduce_colors:
    :param max_colors:
    :param max_w:
    :param max_h:
    :param keep_exif:
    :param convert_all:
    :param conv_big:
    :param force_del:
    :param bg_color:
    :param grayscale:
    :param ignore_size_comparison:
    :param fast_mode:
    :param jobs:
    """
    from optimize_images.__main__ import optimize_batch as optimize

    if output_config is None:
        output_config = OutputConfiguration(show_only_summary=False, show_overall_progress=False, quiet_mode=False)

    message_img_status = optimize(src_path, watch_dir, recursive, quality, remove_transparency, reduce_colors,
                   max_colors, max_w, max_h, keep_exif, convert_all, conv_big, force_del, bg_color,
                   grayscale, ignore_size_comparison, fast_mode, jobs, output_config)
    return message_img_status


def optimize_single_img(task: Task) -> TaskResult:
    """ Try to reduce file size of an image.

       Expects a Task object containing all the parameters for the image processing.

       The actual processing is redirected through do_optimization to the
       corresponding function, according to the detected image format.

       :param task: A Task object containing all the parameters for the image processing.
       :return: A TaskResult object containing information for single file report.
       """
    return do_optimization(task)


# import multiprocessing
#
# if __name__ == '__main__':
#     multiprocessing.freeze_support()
#
#     output_config = OutputConfiguration(show_only_summary=False, show_overall_progress=False, quiet_mode=False)
#     message_img_status, message_report = optimize_as_batch("/Users/danghung/Desktop/optimize-images/tests/themes",
#                       watch_dir=False, recursive=True, quality=65, remove_transparency=False,
#                       reduce_colors=False, max_colors=256, max_w=0, max_h=0, keep_exif=False,
#                       convert_all=True, conv_big=False, force_del=False, bg_color=(255, 255, 255),
#                       grayscale=False, ignore_size_comparison=False, fast_mode=True, jobs=0,
#                       output_config=output_config)
#
#     print(message_img_status, message_report)
