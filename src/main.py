#!/usr/bin/env python3

import editorUI
from uuid import uuid4

ui=editorUI.EditorUI(str(uuid4()) + ".txt")
ui.main()
