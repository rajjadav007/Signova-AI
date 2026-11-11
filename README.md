# Signova AI

AI-Powered Indian Sign Language (ISL) Recognition Application.

Signova AI is an accessibility-focused application designed to bridge communication gaps between individuals who use Indian Sign Language (ISL) and those who do not understand sign language.

## Architecture

```text
Signova-AI/
│
├── frontend/                  # React + JavaScript + Vite
│   ├── public/
│   └── src/
│       ├── assets/
│       ├── components/
│       │   ├── camera/
│       │   ├── recognition/
│       │   ├── translation/
│       │   ├── speech/
│       │   ├── layout/
│       │   └── common/
│       ├── pages/
│       ├── hooks/
│       ├── services/
│       ├── context/
│       ├── utils/
│       ├── styles/
│       ├── App.jsx
│       └── main.jsx
│
├── backend/                   # Python + FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── ai/                        # AI/ML pipeline
│   ├── preprocessing/
│   ├── pose_extraction/
│   ├── inference/
│   ├── model_adapters/
│   ├── postprocessing/
│   └── config/
│
├── models/                    # Model instructions/configs
│   └── README.md
│
├── datasets/                  # Dataset instructions
│   └── README.md
│
├── scripts/                   # Setup and utility scripts
│
├── tests/                     # Cross-module tests
│
├── docs/                      # Project documentation
│
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
