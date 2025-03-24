from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.units import cm
import os
import datetime
from config.config import Config


class PDFGenerator:
    """Generates PDF reports from conversation data"""

    def __init__(self):
        """Initialize with template directory from config"""
        self.template_dir = Config.TEMPLATE_DIR
        self.styles = getSampleStyleSheet()

        # Add custom styles
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",  # Changer 'Title' en 'CustomTitle'
                parent=self.styles["Heading1"],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.navy,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="CustomSection",  # Changer 'Section' en 'CustomSection'
                parent=self.styles["Heading2"],
                fontSize=14,
                spaceAfter=8,
                textColor=colors.navy,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="CustomSubsection",  # Changer 'Subsection' en 'CustomSubsection'
                parent=self.styles["Heading3"],
                fontSize=12,
                spaceAfter=6,
                textColor=colors.navy,
            )
        )

    def generate(self, data, output_path):
        """
        Generate a PDF report from conversation data

        Args:
            data (dict): Conversation data and eligibility result
            output_path (str): Path to save the PDF
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        content = []

        # Add logo if available
        logo_path = os.path.join(self.template_dir, "logo.png")
        if os.path.exists(logo_path):
            logo = Image(logo_path)
            logo.drawHeight = 1.5 * cm
            logo.drawWidth = 4 * cm
            content.append(logo)
            content.append(Spacer(1, 12))

        # Title
        content.append(
            Paragraph(
                "Rapport d'Éligibilité aux Programmes Sociaux",
                self.styles["CustomTitle"],
            )
        )
        content.append(Spacer(1, 12))

        # Date
        date_str = datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")
        content.append(Paragraph(f"Généré le : {date_str}", self.styles["Normal"]))
        content.append(Spacer(1, 12))

        # User Information
        content.append(
            Paragraph("Informations Utilisateur", self.styles["CustomSection"])
        )

        user_data = self._extract_user_data(data)
        user_table_data = [[k, v] for k, v in user_data.items()]

        user_table = Table(user_table_data, colWidths=[150, 300])
        user_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.navy),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (0, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 1, colors.lightgrey),
                ]
            )
        )

        content.append(user_table)
        content.append(Spacer(1, 12))

        # Eligibility Result
        content.append(
            Paragraph("Résultat d'Éligibilité", self.styles["CustomSection"])
        )

        eligibility_result = data.get("eligibility_result", "Non déterminé")
        content.append(
            Paragraph(f"<b>Résultat : </b>{eligibility_result}", self.styles["Normal"])
        )
        content.append(Spacer(1, 12))

        # Program Description
        if eligibility_result in ["ALI", "ML", "PLIE"]:
            content.append(
                Paragraph("Description du Programme", self.styles["CustomSection"])
            )

            program_desc = self._get_program_description(eligibility_result)
            content.append(Paragraph(program_desc, self.styles["Normal"]))
            content.append(Spacer(1, 12))

            # Next Steps
            content.append(Paragraph("Prochaines Étapes", self.styles["CustomSection"]))

            next_steps = self._get_next_steps(eligibility_result)
            for step in next_steps:
                content.append(Paragraph(f"• {step}", self.styles["Normal"]))

            content.append(Spacer(1, 12))

        # Conversation Summary
        content.append(
            Paragraph("Résumé de la Conversation", self.styles["CustomSection"])
        )

        messages = data.get("messages", [])
        convo_table_data = [["Rôle", "Message"]]

        for msg in messages:
            role = msg.get("role", "")
            content_text = msg.get("content", "")

            # Truncate very long messages
            if len(content_text) > 100:
                content_text = content_text[:100] + "..."

            convo_table_data.append([role.capitalize(), content_text])

        convo_table = Table(convo_table_data, colWidths=[80, 370])
        convo_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.navy),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 1, colors.lightgrey),
                ]
            )
        )

        content.append(convo_table)
        content.append(Spacer(1, 12))

        # Footer
        content.append(
            Paragraph(
                "Ce document est généré automatiquement et ne constitue pas une garantie d'éligibilité. Veuillez contacter les services sociaux compétents pour confirmation.",
                self.styles["Normal"],
            )
        )

        # Build the PDF
        doc.build(content)

    def _extract_user_data(self, data):
        """Extract user data from conversation"""
        user_data = {
            "ID Conversation": data.get("id", "N/A"),
            "ID Utilisateur": data.get("user_id", "Anonyme"),
            "Date de création": data.get("created_at", "N/A"),
        }

        # Try to extract more specific data
        messages = data.get("messages", [])
        for msg in messages:
            if msg.get("role") == "user":
                content = msg.get("content", "").lower()

                # Very basic extraction, would be more robust in production
                if "ans" in content and "Âge" not in user_data:
                    import re

                    age_match = re.search(r"\d+", content)
                    if age_match:
                        user_data["Âge"] = age_match.group()

                if "saint-denis" in content and "Ville" not in user_data:
                    user_data["Ville"] = "Saint-Denis"
                elif "stains" in content and "Ville" not in user_data:
                    user_data["Ville"] = "Stains"
                elif "pierrefitte" in content and "Ville" not in user_data:
                    user_data["Ville"] = "Pierrefitte"

                if "rsa" in content and "Bénéficiaire RSA" not in user_data:
                    if "non" in content or "pas" in content:
                        user_data["Bénéficiaire RSA"] = "Non"
                    else:
                        user_data["Bénéficiaire RSA"] = "Oui"

                if "scolarisé" in content and "Scolarisé" not in user_data:
                    if "non" in content or "pas" in content:
                        user_data["Scolarisé"] = "Non"
                    else:
                        user_data["Scolarisé"] = "Oui"

        return user_data

    def _get_program_description(self, program):
        """Get program description based on program type"""
        descriptions = {
            "ALI": """
            Le programme ALI (Accompagnement Logement Insertion) est un dispositif d'accompagnement pour les bénéficiaires du RSA habitant à Saint-Denis, Stains ou Pierrefitte.
            
            Ce programme vise à favoriser l'accès et le maintien dans le logement des personnes en situation de précarité, tout en facilitant leur insertion sociale et professionnelle.
            """,
            "ML": """
            La Mission Locale (ML) est un service public qui accompagne les jeunes de 16 à 25 ans non scolarisés dans leur parcours d'insertion professionnelle et sociale.
            
            Elle propose un suivi personnalisé et global qui couvre l'emploi, la formation, l'orientation, la mobilité, la santé, le logement, l'accès aux droits et aux activités culturelles.
            """,
            "PLIE": """
            Le Plan Local pour l'Insertion et l'Emploi (PLIE) est un dispositif d'accompagnement renforcé pour les adultes de plus de 25 ans et 6 mois qui ne sont pas bénéficiaires du RSA.
            
            Il propose un parcours d'insertion professionnelle individualisé avec un référent unique, des actions de formation, de mise en situation professionnelle et un suivi dans l'emploi.
            """,
        }

        return descriptions.get(
            program, "Description non disponible pour ce programme."
        )

    def _get_next_steps(self, program):
        """Get next steps based on program type"""
        next_steps = {
            "ALI": [
                "Contactez le service ALI au 01.XX.XX.XX.XX pour prendre rendez-vous avec un conseiller.",
                "Préparez vos documents administratifs (pièce d'identité, justificatif de domicile, attestation RSA).",
                "Lors de votre premier rendez-vous, un diagnostic de votre situation sera réalisé.",
                "Un plan d'accompagnement personnalisé vous sera proposé.",
            ],
            "ML": [
                "Rendez-vous à la Mission Locale de votre ville avec une pièce d'identité et un CV si vous en avez un.",
                "Un conseiller vous recevra pour un premier entretien de diagnostic.",
                "Vous serez ensuite orienté vers les services adaptés à votre situation.",
                "Des ateliers collectifs et des rendez-vous individuels vous seront proposés régulièrement.",
            ],
            "PLIE": [
                "Contactez le PLIE au 01.XX.XX.XX.XX pour vous inscrire.",
                "Préparez votre CV et vos documents administratifs.",
                "Un référent unique vous sera attribué pour vous accompagner tout au long de votre parcours.",
                "Des actions de formation et de mise en situation professionnelle vous seront proposées selon votre projet.",
            ],
        }

        return next_steps.get(
            program,
            ["Contactez le service social de votre mairie pour plus d'informations."],
        )
