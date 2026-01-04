#!/usr/bin/env python3
"""Generate a PDF summary of new ROS robotics companies added."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime

def create_pie_chart():
    """Create a pie chart showing company distribution by focus area."""
    drawing = Drawing(300, 180)
    pie = Pie()
    pie.x = 100
    pie.y = 30
    pie.width = 100
    pie.height = 100
    pie.data = [3, 2, 1, 1]
    pie.labels = ['Humanoid', 'Warehouse', 'Security', 'Navigation']
    pie.slices[0].fillColor = colors.HexColor('#4CAF50')
    pie.slices[1].fillColor = colors.HexColor('#2196F3')
    pie.slices[2].fillColor = colors.HexColor('#FF9800')
    pie.slices[3].fillColor = colors.HexColor('#9C27B0')
    drawing.add(pie)
    return drawing

def create_bar_chart():
    """Create a bar chart showing companies by founding year."""
    drawing = Drawing(350, 150)
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 30
    bc.height = 100
    bc.width = 250
    bc.data = [[1, 2, 1, 2, 1]]  # 2014, 2015, 2016, 2018, 2020
    bc.categoryAxis.categoryNames = ['2014', '2015', '2016', '2018', '2020']
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 3
    bc.bars[0].fillColor = colors.HexColor('#2196F3')
    drawing.add(bc)
    return drawing

def create_report():
    output_path = "/home/user/ros-robotics-companies/new_companies_report.pdf"
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#0066CC'),
        spaceAfter=20,
        alignment=1  # Center
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray,
        spaceAfter=20,
        alignment=1
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceBefore=15,
        spaceAfter=10,
        backColor=colors.HexColor('#E6F0FA')
    )

    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#006699'),
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        spaceAfter=5
    )

    ros_style = ParagraphStyle(
        'ROSUsage',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#008000'),
        leftIndent=10,
        spaceBefore=2,
        spaceAfter=8
    )

    elements = []

    # Title
    elements.append(Paragraph("ROS Robotics Companies", title_style))
    elements.append(Paragraph("New Additions Report", title_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", subtitle_style))

    # Executive Summary
    elements.append(Paragraph("Executive Summary", heading_style))
    elements.append(Paragraph(
        "This report summarizes research conducted to identify new ROS/ROS 2 robotics "
        "companies for inclusion in the ros-robotics-companies repository. A total of "
        "<b>7 new companies</b> were identified and added, bringing the total count from "
        "<b>722 to 729</b>.",
        body_style
    ))

    elements.append(Spacer(1, 10))

    # Statistics Table
    elements.append(Paragraph("Quick Statistics", heading_style))
    stats_data = [
        ['Metric', 'Value'],
        ['Previous Count', '722'],
        ['Companies Added', '7'],
        ['New Total', '729'],
        ['Branch', 'claude/search-more-candidates-4wtLh']
    ]
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 15))

    # New Companies Section
    elements.append(Paragraph("New Companies Added", heading_style))

    companies = [
        {
            "name": "1X Technologies",
            "year": "2014",
            "location": "Norway/USA",
            "description": "Norwegian-American robotics company developing NEO, a bipedal humanoid robot for home environments. Uses NVIDIA Isaac and GR00T for AI development. Formerly known as Halodi Robotics.",
            "ros_usage": "ROS support through NVIDIA Isaac integration"
        },
        {
            "name": "Agility Robotics",
            "year": "2015",
            "location": "USA",
            "description": "Develops bipedal humanoid robots for warehouse and logistics. Their Digit robot runs on ROS and Linux OS with real-time control. Partnered with Amazon and GXO Logistics.",
            "ros_usage": "ROS on Linux OS with real-time control loops"
        },
        {
            "name": "Fourier Intelligence",
            "year": "2015",
            "location": "China",
            "description": "General-purpose robotics company developing GR-1 and GR-2 humanoid robots. Released open-source humanoid robot Fourier N1.",
            "ros_usage": "ROS-compatible SDK, Mujoco, NVIDIA Isaac Lab support"
        },
        {
            "name": "KABAM Robotics",
            "year": "2018",
            "location": "Singapore",
            "description": "Develops autonomous security robots including Matrix (outdoor) and Co-Lab (indoor) for 24/7 surveillance with real-time video analytics.",
            "ros_usage": "ROS 2 Jazzy with NVIDIA Jetson AGX Orin"
        },
        {
            "name": "Open Navigation LLC",
            "year": "2020",
            "location": "USA",
            "description": "Provides project leadership, maintenance, and support to the Nav2 & ROS community. Nav2 is trusted by 100+ companies worldwide.",
            "ros_usage": "Core maintainer of Nav2 (ROS 2 Navigation Stack)"
        },
        {
            "name": "Richtech Robotics",
            "year": "2016",
            "location": "USA",
            "description": "Develops ADAM robot bartender. Deployed at NHL arenas and MLB stadiums for automated beverage service.",
            "ros_usage": "NVIDIA Jetson AGX Orin with Isaac ROS 2 libraries"
        },
        {
            "name": "Sereact",
            "year": "2020",
            "location": "Germany",
            "description": "AI robotics company automating warehouse pick-and-pack with vision language action models. PickGPT enables natural language robot instruction.",
            "ros_usage": "Hiring ROS 2 engineers, works with major robot manufacturers"
        }
    ]

    for i, company in enumerate(companies, 1):
        elements.append(Paragraph(f"{i}. {company['name']} ({company['year']}) - {company['location']}", subheading_style))
        elements.append(Paragraph(company['description'], body_style))
        elements.append(Paragraph(f"<b>ROS Usage:</b> {company['ros_usage']}", ros_style))

    # Charts
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Distribution by Focus Area", heading_style))
    elements.append(create_pie_chart())

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Companies by Founding Year", heading_style))
    elements.append(create_bar_chart())

    # Key Findings
    elements.append(Paragraph("Key Research Findings", heading_style))
    findings = [
        "NVIDIA Isaac ROS 2 is becoming a common platform for advanced robotics companies",
        "Humanoid robotics is a rapidly growing sector with multiple companies using ROS",
        "Many companies are transitioning from ROS 1 to ROS 2 for production systems",
        "Security and warehouse automation are key application areas for ROS-based robots",
        "Open-source contributions remain important (Nav2, Isaac ROS, Gazebo)"
    ]
    for finding in findings:
        elements.append(Paragraph(f"• {finding}", bullet_style))

    # Companies Not Added
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Companies Researched But Not Added", heading_style))
    elements.append(Paragraph(
        "The following were researched but not added because they either already exist "
        "in the list (NEURA Robotics, Flexiv, Unitree), don't explicitly confirm ROS usage "
        "(Figure AI, Covariant, Symbotic), or use proprietary systems (Keenon, Pudu).",
        body_style
    ))

    # Build PDF
    doc.build(elements)
    print(f"PDF report saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    create_report()
