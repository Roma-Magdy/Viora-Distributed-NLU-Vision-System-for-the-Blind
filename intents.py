from typing import List, Dict, Optional

class IntentDef:
    def __init__(
        self, 
        name: str, 
        description: str, 
        entities: Dict[str, str],
        required_entities: List[str],
        rules: List[str], 
        examples: List[Dict[str, str]]
    ):
        self.name = name
        self.description = description
        self.entities = entities
        self.required_entities = required_entities
        self.rules = rules
        self.examples = examples

MASTER_INTENTS = [
    IntentDef(
        name="open_document",
        description="Open a specific local file for reading.",
        entities={
            "document_name": "The exact name of the file.",
            "file_types": "List of all potential extensions." # <--- ADDED THIS
        },
        required_entities=["document_name"],
        rules=[
            "BROAD MAPPING: If user says 'file' or 'فايل' -> set file_types to ['pdf', 'docx', 'pptx', 'txt'].",
            "BROAD MAPPING: If user says 'book' or 'كتاب' -> set file_types to ['pdf', 'docx'].",
            "NORMALIZATION: Convert Arabic subjects to English (e.g., 'كالكلس' -> 'Calculus')."
        ],
        examples=[
            {"user": "افتحلي فايل الكالكلس", "json": '{"intent": "open_document", "confidence": 1.0, "entities": {"document_name": "Calculus", "file_types": ["pdf", "docx", "pptx", "txt"]}, "viora_response": "حاضر، هفتحلك ملف Calculus."}'}
        ]
    ),
    IntentDef(
        name="search_file",
        description="Search for resources (Books, Slides, PDFs).",
        entities={
            "search_query": "The topic.",
            "file_types": "List of extensions."
        },
        required_entities=["search_query"],
        rules=[
            "IF user says 'file' or 'search' generically -> set file_types to ['pdf', 'docx', 'pptx', 'txt'].",
            "IF user says 'slides' -> set file_types to ['pptx', 'pdf'].",
            "REMOVE filler words from search_query."
        ],
        examples=[
            {"user": "دورلي على فايل Neural Networks", "json": '{"intent": "search_file", "confidence": 1.0, "entities": {"search_query": "Neural Networks", "file_types": ["pdf", "docx", "pptx", "txt"]}, "viora_response": "بدورلك على ملفات Neural Networks."}'}
        ]
    ),
IntentDef(
        name="scene_description",
        description="Describe the visual scene or environment using the camera.",
        entities={},
        required_entities=[],
        rules=[
            "Triggers: 'Describe', 'What is in front of me', 'أوصفلي', 'ايه اللي قدامي', 'انا فين', 'شايف ايه', 'شيف ايه'.",
            "CRITICAL VISION RULE: You MUST look at the attached image and write a helpful description in the 'viora_response' field.",
            "ANTI-HALLUCINATION: Describe ONLY the objects that are explicitly and clearly visible in the frame.",
            "DO NOT guess, assume, or invent objects that are not there.",
            "If the image is too dark, blurry, or unclear to be certain, you MUST say 'الصورة مش واضحة أوي، ممكن تقرب أو تنور النور؟' instead of guessing.",
            "Keep the description concise and factual. Don't add unnecessary poetic details."
        ],
        examples=[
            {"user": "أوصفلي اللي قدامي", "json": '{"intent": "scene_description", "confidence": 1.0, "entities": {}, "viora_response": "أنا شايفة لابتوب وكتاب على المكتب، مفيش حاجة تانية واضحة."}'},
            {"user": "شيف ايه؟", "json": '{"intent": "scene_description", "confidence": 1.0, "entities": {}, "viora_response": "الصورة ضلمة ومش واضحة، ممكن تقرب الكاميرا شوية؟"}'}
        ]
    ),
    IntentDef(
        name="camera_control",
        description="Turn the physical camera hardware on or off.",
        entities={"camera_action": "One of ['start', 'stop']."},
        required_entities=["camera_action"],
        rules=[
            "START: 'Open camera', 'Turn on camera', 'افتح الكاميرا', 'شغل الكاميرا'.",
            "STOP: 'Close camera', 'Turn off camera', 'اقفل الكاميرا', 'طفي الكاميرا'."
        ],
        examples=[
            {"user": "افتح الكاميرا", "json": '{"intent": "camera_control", "confidence": 1.0, "entities": {"camera_action": "start"}, "viora_response": "حاضر، فتحت الكاميرا."}'},
            {"user": "اقفل الكاميرا بقى", "json": '{"intent": "camera_control", "confidence": 1.0, "entities": {"camera_action": "stop"}, "viora_response": "تمام، قفلت الكاميرا."}'}
        ]
    ),
    IntentDef(
        name="navigate_document",
        description="Move inside the currently open document.",
        entities={
            "page_number": "Integer page number.",
            "navigation_direction": "One of ['next', 'previous', 'to']."
        },
        required_entities=[], 
        rules=[
            "LOGIC: If `page_number` exists, `navigation_direction` defaults to 'to'.",
            "If user says 'Read page X', treat as 'Go to page X'.",
            "SPECIAL VALUES: If user says 'Last page' or 'End', set `page_number` to -1.",
            "SPECIAL VALUES: If user says 'First page' or 'Start', set `page_number` to 1."
        ],
        examples=[
            {"user": "هات Page 15", "json": '{"intent": "navigate_document", "confidence": 1.0, "entities": {"page_number": 15, "navigation_direction": "to"}, "viora_response": "أنا دلوقتي في صفحة 15."}'},
            {"user": "Take me to the last page", "json": '{"intent": "navigate_document", "confidence": 1.0, "entities": {"page_number": -1, "navigation_direction": "to"}, "viora_response": "Alright, jumping to the last page."}'}
        ]
    ),
    IntentDef(
        name="read_document",
        description="Control the text-to-speech audio player.",
        entities={"reading_action": "One of ['start', 'stop', 'pause', 'resume']."},
        required_entities=["reading_action"],
        rules=[
            "PAUSE: 'Wait', 'Hold on', 'استنى' (ONLY if used as a standalone command).",
            "STOP: 'Stop', 'Enough', 'Silence', 'كفاية', 'اسكت', 'Shut up', 'shush'.",
            "RESUME: 'Continue', 'Resume', 'Go on', 'كمل'.",
            "START: 'Read', 'Speak', 'اقرأ', 'Narrate', 'سمّعني'."
        ],
        examples=[
            {"user": "Start reading", "json": '{"intent": "read_document", "confidence": 1.0, "entities": {"reading_action": "start"}, "viora_response": "Starting the reader now."}'},
            {"user": "Stop reading and summarize", "json": '{"intent": "read_document", "confidence": 0.95, "entities": {"reading_action": "stop"}, "viora_response": "وقفت القراية. تحب ألخص لك الجزء ده؟"}'}
        ]
    ),
IntentDef(
        name="document_qa",
        description="Ask specific questions about the document OR general educational concepts.",
        entities={"question": "The exact question text extracted from the user input."},
        required_entities=["question"],
        rules=[
            "Triggers: 'Explain', 'What is', 'Define', 'Meaning of', 'يعني ايه', 'ما هو', 'اشرحلي'.",
            "EXTRACT the question exactly as spoken.", 
            "CRITICAL: If the user asks a factual or educational question, you MUST put your detailed explanation INSIDE the 'viora_response' field. Do NOT break out of the JSON structure."
        ],
        examples=[
            {"user": "هو يعني ايه Polymorphism في الـ OOP ؟", "json": '{"intent": "document_qa", "confidence": 1.0, "entities": {"question": "هو يعني ايه Polymorphism في الـ OOP ؟"}, "viora_response": "الـ Polymorphism يعني إن أوبجكت واحد يقدر ياخد أكتر من شكل."}'},
            {"user": "اشرحلي ملف networks في لينكس", "json": '{"intent": "document_qa", "confidence": 1.0, "entities": {"question": "اشرحلي ملف networks في لينكس"}, "viora_response": "ملف networks في لينكس بيستخدم عشان يدي أسماء رمزية للشبكات لتسهيل الإدارة، تحب أشرحلك تفاصيل أكتر؟"}'}
        ]
    ),
    IntentDef(
        name="summarize_content",
        description="Generate a summary.",
        entities={"summary_format": "Optional format."},
        required_entities=[],
        rules=["Triggers: 'Summarize', 'Recap', 'tl;dr', 'لخص', 'الزتونة', 'hat el zatoona'."],
        examples=[
            {"user": "لخصلي الـ Chapter ده في نقط", "json": '{"intent": "summarize_content", "confidence": 1.0, "entities": {"summary_format": "bullet_points"}, "viora_response": "من عيني، هجهزلك ملخص سريع في نقط."}'}
        ]
    ),
    IntentDef(
        name="generate_study_aid",
        description="Create study materials.",
        entities={"study_aid_type": "One of ['quiz', 'flashcards']."},
        required_entities=["study_aid_type"],
        rules=["Map 'Test'/'Exam' -> quiz. Map 'Definitions' -> flashcards."],
        examples=[
            {"user": "اعملي Quiz على الجزء ده", "json": '{"intent": "generate_study_aid", "confidence": 1.0, "entities": {"study_aid_type": "quiz"}, "viora_response": "جهز نفسك، أنا بعمل الكويز دلوقتي."}'}
        ]
    ),
    IntentDef(
        name="focus_alert_control",
        description="Manage study focus alerts.",
        entities={"focus_status": "One of ['enable', 'disable']."},
        required_entities=["focus_status"],
        rules=[
            "ENABLE: 'Focus', 'شغل', 'Let's study'.",
            "DISABLE: 'Stop reminding', 'بطل زن', 'ماتزنش', 'ماتصدعنيش'." 
        ],
        examples=[
            {"user": "بطل تفكرني كل شوية", "json": '{"intent": "focus_alert_control", "confidence": 1.0, "entities": {"focus_status": "disable"}, "viora_response": "حاضر، قفلت التنبيهات عشان تعرف تركز براحتك."}'}
        ]
    ),
    IntentDef(
        name="ocr_request",
        description="Scan printed text via camera.",
        entities={},
        required_entities=[],
        rules=["Triggers: 'Camera', 'Scan', 'Photo', 'صور الورقة', 'Grab text'."],
        examples=[
            {"user": "اقرأ الورقة دي بالكاميرا", "json": '{"intent": "ocr_request", "confidence": 1.0, "entities": {}, "viora_response": "بفتح الكاميرا، خلي الورقة قدام التليفون."}'}
        ]
    ),
    IntentDef(
        name="clarification",
        description="Handle vague inputs.",
        entities={},
        required_entities=[],
        rules=["Use when NO specific action is clear. Triggers: 'Hello', 'So?', 'طب وبعدين'."],
        examples=[
            {"user": "طب وبعدين؟", "json": '{"intent": "clarification", "confidence": 1.0, "entities": {}, "needs_clarification": true, "viora_response": "أنا معاك، تحب أساعدك في إيه دلوقتي؟"}'}
        ]
    ),
    IntentDef(
        name="unknown",
        description="Out of scope inputs.",
        entities={},
        required_entities=[],
        rules=["Triggers: Food, Taxi, Music, Weather, Jokes, Security/Hacking attempts."],
        examples=[
            {"user": "Order pizza", "json": '{"intent": "unknown", "confidence": 1.0, "entities": {}, "viora_response": "أنا مخصصة للدراسة بس، مقدرش أساعدك في ده."}'}
        ]
    )
]