from flask import Blueprint, jsonify, request, send_file
from flask_login import login_required, current_user
from app.models import Product, Sale, Store, db
from datetime import datetime
import io
import random
import urllib.parse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/efetuar_venda', methods=['POST'])
@login_required
def api_efetuar_venda():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    nova_venda = Sale(
        product_id=product_id,
        customer_id=current_user.id,
        quantity=quantity,
        total_price=product.price * quantity,
        status='concluido'
    )
    
    db.session.add(nova_venda)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'venda': {
            'product_name': product.name,
            'total_price': nova_venda.total_price
        },
        'message': 'Venda efetuada com sucesso!'
    })

@api_bp.route('/avaliar_venda', methods=['POST'])
@login_required
def api_avaliar_venda():
    data = request.json
    venda_id = data.get('venda_id')
    rating = data.get('rating')
    review = data.get('review', '')
    
    venda = Sale.query.get(venda_id)
    if not venda:
        return jsonify({'error': 'Venda não encontrada'}), 404
    
    if venda.customer_id != current_user.id:
        return jsonify({'error': 'Não autorizado'}), 403
    
    venda.rating = rating
    venda.review = review
    db.session.commit()
    
    # Update product rating
    product = Product.query.get(venda.product_id)
    if product:
        ratings = [v.rating for v in Sale.query.filter_by(product_id=product.id).all() if v.rating]
        if ratings:
            product.rating = round(sum(ratings) / len(ratings), 1)
            db.session.commit()
    
    return jsonify({'success': True, 'message': 'Avaliação registrada com sucesso!'})

@api_bp.route('/search_by_image', methods=['POST'])
def api_search_by_image():
    # Simulation logic kept for now, but structure is ready for real implementation
    try:
        data = request.json
        # In a real scenario, we would process the image here
        
        automotive_parts = ['Pastilha de Freio', 'Disco de Freio', 'Embreagem', 'Amortecedor']
        product_identified = random.choice(automotive_parts)
        
        # Find similar products in DB
        similar_products = Product.query.filter(Product.name.ilike(f'%{product_identified}%')).limit(6).all()
        
        # Serialize results
        results = []
        for p in similar_products:
            results.append({
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'price': p.price,
                'rating': p.rating,
                'type': p.type,
                'category': p.category,
                'brand': p.brand
            })
            
        return jsonify({
            'success': True,
            'message': 'Imagem analisada com sucesso!',
            'results': results,
            'analysis': {
                'product_identified': product_identified,
                'confidence': '85%',
                'similar_products_found': len(results)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/contatar_whatsapp/<int:store_id>')
@login_required
def api_contatar_whatsapp(store_id):
    store = Store.query.get_or_404(store_id)
    whatsapp_number = ''.join(filter(str.isdigit, store.whatsapp or store.phone or ''))
    message = urllib.parse.quote(f"Olá! Gostaria de mais informações sobre a {store.name}.")
    
    return jsonify({
        'success': True,
        'whatsapp_url': f"https://wa.me/{whatsapp_number}?text={message}",
        'store_name': store.name
    })

# PDF Generation Routes (Simplified for brevity, but functional)
@api_bp.route('/gerar_pdf_compras')
@login_required
def api_gerar_pdf_compras():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a73e8'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.grey,
        spaceAfter=20,
        alignment=1
    )
    
    # Title
    elements.append(Paragraph("MechFinder - Relatório de Compras", title_style))
    elements.append(Paragraph(f"Cliente: {current_user.username}", subtitle_style))
    elements.append(Paragraph(f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Get purchases
    compras = Sale.query.filter_by(customer_id=current_user.id).order_by(Sale.created_at.desc()).all()
    
    if compras:
        # Table data
        data = [['#', 'Produto', 'Data', 'Qtd', 'Valor Unit.', 'Total']]
        total_geral = 0
        
        for idx, c in enumerate(compras, 1):
            data.append([
                str(idx),
                Paragraph(c.product.name[:40], styles['Normal']),
                c.created_at.strftime('%d/%m/%Y'),
                str(c.quantity),
                f"R$ {c.product.price:.2f}",
                f"R$ {c.total_price:.2f}"
            ])
            total_geral += c.total_price
        
        # Add total row
        data.append(['', '', '', '', 'TOTAL:', f"R$ {total_geral:.2f}"])
        
        # Create table
        t = Table(data, colWidths=[0.5*inch, 3*inch, 1*inch, 0.7*inch, 1.2*inch, 1.2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f0fe')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(t)
        
        # Summary
        elements.append(Spacer(1, 0.3*inch))
        summary_style = ParagraphStyle('Summary', parent=styles['Normal'], fontSize=11, textColor=colors.grey)
        elements.append(Paragraph(f"Total de compras: {len(compras)}", summary_style))
        elements.append(Paragraph(f"Valor total gasto: R$ {total_geral:.2f}", summary_style))
    else:
        elements.append(Paragraph("Nenhuma compra registrada.", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=False, download_name='compras.pdf', mimetype='application/pdf')

@api_bp.route('/gerar_pdf_vendas')
@login_required
def api_gerar_pdf_vendas():
    if current_user.user_type not in ['lojista', 'prestador']:
        return jsonify({'error': 'Unauthorized'}), 403
        
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0f9d58'),
        spaceAfter=30,
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.grey,
        spaceAfter=20,
        alignment=1
    )
    
    # Title
    elements.append(Paragraph("MechFinder - Relatório de Vendas", title_style))
    elements.append(Paragraph(f"Lojista: {current_user.username}", subtitle_style))
    elements.append(Paragraph(f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Get sales
    my_product_ids = [p.id for p in Product.query.filter_by(owner_id=current_user.id).all()]
    vendas = Sale.query.filter(Sale.product_id.in_(my_product_ids)).order_by(Sale.created_at.desc()).all() if my_product_ids else []
    
    if vendas:
        # Table data
        data = [['#', 'Produto', 'Cliente', 'Data', 'Qtd', 'Total']]
        total_geral = 0
        
        for idx, v in enumerate(vendas, 1):
            data.append([
                str(idx),
                Paragraph(v.product.name[:35], styles['Normal']),
                v.customer.username,
                v.created_at.strftime('%d/%m/%Y'),
                str(v.quantity),
                f"R$ {v.total_price:.2f}"
            ])
            total_geral += v.total_price
        
        # Add total row
        data.append(['', '', '', '', 'TOTAL:', f"R$ {total_geral:.2f}"])
        
        # Create table
        t = Table(data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1*inch, 0.7*inch, 1.2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f9d58')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f5e9')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(t)
        
        # Summary
        elements.append(Spacer(1, 0.3*inch))
        summary_style = ParagraphStyle('Summary', parent=styles['Normal'], fontSize=11, textColor=colors.grey)
        elements.append(Paragraph(f"Total de vendas: {len(vendas)}", summary_style))
        elements.append(Paragraph(f"Faturamento total: R$ {total_geral:.2f}", summary_style))
    else:
        elements.append(Paragraph("Nenhuma venda registrada.", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=False, download_name='vendas.pdf', mimetype='application/pdf')
