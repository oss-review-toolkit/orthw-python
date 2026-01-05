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

from rich import print as rprint

from orthw.utils.cmdgroups import command_group


def scan_results() -> None:
    """Update the ORTHW project or its components.

    This function is intended to handle update operations for the ORTHW project.
    Currently, it is not implemented.
    """
    rprint("\n[sandy_brown]This command is not implemented yet.[/sandy_brown]")


@command_group.command(
    name="scan-results",
    context="SCAN_CONTEXT",
)
def __scan_results() -> None:
    scan_results()
