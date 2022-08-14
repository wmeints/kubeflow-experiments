import os
import kfp
from kfp import dsl
import kfp.components as comp


def relative_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


minio_download = comp.load_component_from_file(relative_path("../../components/minio-download/component.yaml"))
feature_selection = comp.load_component_from_file(relative_path("../../components/feature-selection/component.yaml"))
fix_missing_values = comp.load_component_from_file(relative_path("../../components/fix-missing-values/component.yaml"))
minio_upload = comp.load_component_from_file(relative_path("../../components/minio-upload/component.yaml"))


@dsl.pipeline(
    name="Prepare dataset"
)
def prepare_data():
    download_step = minio_download(
        bucket="datalake",
        path="raw/wachttijden/2022/08/14/wachttijden.csv"
    )

    feature_selection_step = feature_selection(
        input=download_step.outputs["output"]
    )

    fix_missing_values_step = fix_missing_values(
        input=feature_selection_step.outputs["output"]
    )

    minio_upload_step = minio_upload(
        bucket="datalake",
        path="preprocessed/wachttijden/2022/08/14/wachttijden.csv",
        input=fix_missing_values_step.outputs["output"]
    )


if __name__ == "__main__":
    pipeline_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline.yaml")
    kfp.compiler.Compiler().compile(pipeline_func=prepare_data, package_path=pipeline_path)