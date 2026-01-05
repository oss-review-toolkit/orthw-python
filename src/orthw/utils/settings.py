# Copyright 2023 The ORTHW Project Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE
from pathlib import Path
from typing import ClassVar

import tomli_w
from platformdirs import user_data_dir
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, TomlConfigSettingsSource


class Settings(BaseSettings):
    """Base config object. Reads default orthw config file or set default."""

    ORTHW_CONFIG_DIR: ClassVar[Path] = Path(user_data_dir("orthw"))
    ORTHW_CONFIG_FILE: ClassVar[Path] = ORTHW_CONFIG_DIR / "orthwconfig"
    model_config = SettingsConfigDict(
        extra="ignore",
        toml_file=ORTHW_CONFIG_FILE,
    )

    configuration_home: Path = ORTHW_CONFIG_DIR / "ort-config"
    enabled_advisors: str | None = "osv"
    exports_home: Path = ORTHW_CONFIG_DIR / "exports"
    gitlab_host: str | None = "gitlab.example.com"
    gitlab_token: str | None = None
    ignore_excluded_rule_ids: str | None = None
    netrc_login: str | None = None
    netrc_machine: str | None = None
    netrc_password: str | None = None
    non_offending_license_categories: str | None = None
    non_offending_license_ids: str | None = None
    ort_docker_image: str = "ghcr.io/oss-review-toolkit/ort:latest"
    ort_docker_registry_password: str | None = None
    ort_docker_registry_server: str | None = None
    ort_docker_registry_username: str | None = None
    ort_home: Path = ORTHW_CONFIG_DIR / "ort"
    ort_jvm_options: str | None = "-Xmx16G"
    ort_options: str | None = "--info"
    orth_jvm_options: str | None = "-Xmx16G"
    orth_options: str | None = None
    scancode_home: Path = ORTHW_CONFIG_DIR / "scancode-toolkit"
    scancode_version: str = "32.1.0"
    scandb_db: str | None = None
    scandb_host: str | None = None
    scandb_password: str | None = None
    scandb_port: str | None = None
    scandb_schema: str | None = None
    scandb_user: str | None = None

    # Config directory files
    evaluation_md5_sum_file: Path = ORTHW_CONFIG_DIR / "evaluation-md5sum.txt"
    evaluation_result_file: Path = ORTHW_CONFIG_DIR / "evaluation-result.json"
    package_configuration_md5_sum_file: Path = ORTHW_CONFIG_DIR / "package-configuration-md5sum.txt"
    package_curations_md5_sum_file: Path = ORTHW_CONFIG_DIR / "package-curations-md5sum.txt"
    scan_result_file: Path = ORTHW_CONFIG_DIR / "scan-result.json"
    scan_results_storage_dir: Path = ORTHW_CONFIG_DIR / "scan-results"
    target_url_file: Path = ORTHW_CONFIG_DIR / "target-url.txt"
    temp_dir: Path = ORTHW_CONFIG_DIR / "tmp"

    # Configuration (repository) files
    ort_config_copyright_garbage_file: Path = configuration_home / "copyright-garbage.yml"
    ort_config_custom_license_texts_dir: Path = configuration_home / "custom-license-texts"
    ort_config_how_to_fix_text_provider_script: Path = configuration_home / "how-to-fix-text-provider.kts"
    ort_config_license_classifications_file: Path = configuration_home / "license-classifications.yml"
    ort_config_notice_templates_dir: Path = configuration_home / "notice-templates"
    ort_config_package_configurations_dir: Path = configuration_home / "package-configurations"
    ort_config_package_curations_dir: Path = configuration_home / "curations"
    ort_config_resolutions_file: Path = configuration_home / "resolutions.yml"
    ort_config_rules_file: Path = configuration_home / "evaluator.rules.kts"

    # Exports (repository) files
    exports_license_finding_curations_file: Path = exports_home / "license-finding-curations.yml"
    exports_path_excludes_file: Path = exports_home / "path-excludes.yml"
    exports_vcs_url_mapping_file: Path = exports_home / "vcs-url-mapping.yml"

    # Initialized orthw directory input / output files:
    copyrights_debug_file: Path = Path("copyrights-debug.txt")
    copyrights_file: Path = Path("copyrights.txt")
    cyclone_dx_report_file: Path = Path("cyclone-dx-report.xml")
    evaluated_model_report_file: Path = Path("evaluated-model.json")
    gitlab_license_model_report_file: Path = Path("gl-license-scanning-report.json")
    html_report_file: Path = Path("report.html")
    repository_configuration_file: Path = Path("ort.yml")
    spdx_json_report_file: Path = Path("report.spdx.json")
    spdx_yaml_report_file: Path = Path("report.spdx.yml")
    webapp_report_file: Path = Path("webapp.html")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize the order of settings sources for Pydantic configuration.

        This method overrides the default settings sources to use only the TOML config file
        specified in the model_config. Other sources such as environment variables, .env files,
        and file secrets are ignored.

        Args:
            settings_cls: The settings class being configured.
            init_settings: Source for settings passed to the initializer.
            env_settings: Source for settings from environment variables.
            dotenv_settings: Source for settings from .env files.
            file_secret_settings: Source for settings from file secrets.

        Returns:
            A tuple containing only the TomlConfigSettingsSource for the settings class.

        """
        return (
            init_settings,
            TomlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


def load_settings() -> Settings:
    """Load the application settings from the default configuration file.

    This function ensures that the configuration directory and file exist.
    If the configuration file does not exist, it creates one with default settings.
    Finally, it returns an instance of the Settings class loaded from the config file.

    Returns:
        Settings: An instance of the Settings class with loaded configuration.

    """
    config_file = Settings.ORTHW_CONFIG_FILE
    config_dir = config_file.parent

    config_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not config_file.exists():
        _write_default_config(config_file)

    return Settings()


def _write_default_config(config_file: Path) -> None:
    """Create a new config file by dumping the Settings model defaults.

    This MUST NOT read from any existing config sources.
    """
    defaults = Settings(
        model_config=SettingsConfigDict(
            toml_file=None,
        )
    )

    data = defaults.model_dump(
        mode="json",
        exclude_none=True,  # optional, usually desirable
    )

    config_file.write_text(tomli_w.dumps(data))
