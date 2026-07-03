# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the vLLM project

"""Tiny JSONL event hook for CoherentKV experiments.

This module is inert unless CKV_VLLM_EVENT_LOG is set. It is intentionally
minimal so experimental observability patches do not change normal vLLM paths.
"""

import json
import os
import time
from typing import Any


def emit_ckv_event(
    event_type: str,
    request_id: str | None = None,
    data: dict[str, Any] | None = None,
) -> None:
    path = os.environ.get("CKV_VLLM_EVENT_LOG")
    if not path:
        return

    event = {
        "event_type": event_type,
        "ts": time.time(),
        "request_id": request_id,
        "source": "vllm",
        "data": data or {},
    }
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
