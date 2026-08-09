from flask import request, jsonify
from flask_login import login_required, current_user
from models import Category
from models import db
from utils.decorators import admin_required, role_required
from sqlalchemy import or_

class CategoryController:
    """Controller for category management operations"""
    
    @staticmethod
    def validate_category_name(name):
        """Validate category name"""
        return name and len(name.strip()) >= 2
    
    @staticmethod
    def validate_category_code(code):
        """Validate category code"""
        return code and len(code.strip()) >= 2 and code.isalnum()
    
    # =============================================
    # CREATE CATEGORY
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def create_category():
        """Create a new category"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data.get('category_name'):
                return jsonify({'error': 'Category name is required'}), 400
            if not data.get('category_code'):
                return jsonify({'error': 'Category code is required'}), 400
            
            # Validate name
            if not CategoryController.validate_category_name(data['category_name']):
                return jsonify({'error': 'Category name must be at least 2 characters'}), 400
            
            # Validate code
            if not CategoryController.validate_category_code(data['category_code']):
                return jsonify({'error': 'Category code must be at least 2 characters and alphanumeric'}), 400
            
            # Check if category name exists
            if Category.query.filter_by(category_name=data['category_name'].strip()).first():
                return jsonify({'error': 'Category name already exists'}), 400
            
            # Check if category code exists
            if Category.query.filter_by(category_code=data['category_code'].strip().upper()).first():
                return jsonify({'error': 'Category code already exists'}), 400
            
            # Validate parent category if provided
            parent_id = data.get('parent_category_id')
            if parent_id:
                parent = Category.query.get(parent_id)
                if not parent:
                    return jsonify({'error': 'Parent category not found'}), 400
                if parent.status != 'Active':
                    return jsonify({'error': 'Parent category is not active'}), 400
                # Prevent circular reference
                if parent.parent_category_id == parent_id:
                    return jsonify({'error': 'Circular reference detected'}), 400
            
            # Create category
            category = Category(
                category_name=data['category_name'].strip(),
                category_code=data['category_code'].strip().upper(),
                description=data.get('description', '').strip() if data.get('description') else None,
                icon=data.get('icon', '').strip() if data.get('icon') else None,
                display_order=data.get('display_order', 0),
                status=data.get('status', 'Active'),
                parent_category_id=parent_id
            )
            
            db.session.add(category)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Category created successfully',
                'data': category.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # =============================================
    # READ CATEGORIES (List with Hierarchy)
    # =============================================
    
    @staticmethod
    @login_required
    def list_categories():
        """List all categories with hierarchy"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 50, type=int)
            search = request.args.get('search', '')
            status = request.args.get('status', '')
            include_subcategories = request.args.get('include_subcategories', 'true').lower() == 'true'
            parent_id = request.args.get('parent_id', type=int)
            
            # Build query
            query = Category.query
            
            # Apply search filter
            if search:
                query = query.filter(
                    (Category.category_name.ilike(f'%{search}%')) |
                    (Category.category_code.ilike(f'%{search}%')) |
                    (Category.description.ilike(f'%{search}%'))
                )
            
            # Apply status filter
            if status and status != '':
                query = query.filter(Category.status == status)
            
            # Apply parent filter
            if parent_id is not None:
                query = query.filter(Category.parent_category_id == parent_id)
            elif not include_subcategories:
                # Only get root categories (no parent)
                query = query.filter(Category.parent_category_id.is_(None))
            
            # Order by display order and name
            query = query.order_by(Category.display_order, Category.category_name)
            
            # Paginate
            categories = query.paginate(page=page, per_page=per_page, error_out=False)
            
            # Build hierarchical tree if requested
            if include_subcategories and not parent_id:
                root_categories = Category.query.filter(
                    Category.parent_category_id.is_(None),
                    Category.status == 'Active' if not status else Category.status == status
                ).order_by(Category.display_order).all()
                
                category_tree = []
                for root in root_categories:
                    category_tree.append(CategoryController._build_category_tree(root))
                
                return jsonify({
                    'success': True,
                    'data': [cat.to_dict() for cat in categories.items],
                    'category_tree': category_tree,
                    'total': categories.total,
                    'page': categories.page,
                    'per_page': categories.per_page,
                    'pages': categories.pages
                }), 200
            
            return jsonify({
                'success': True,
                'data': [cat.to_dict() for cat in categories.items],
                'total': categories.total,
                'page': categories.page,
                'per_page': categories.per_page,
                'pages': categories.pages
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @staticmethod
    def _build_category_tree(category):
        """Recursively build category tree"""
        children = Category.query.filter_by(
            parent_category_id=category.category_id,
            status='Active'
        ).order_by(Category.display_order).all()
        
        return {
            'category': category.to_dict(),
            'children': [CategoryController._build_category_tree(child) for child in children]
        }
    
    # =============================================
    # READ SINGLE CATEGORY
    # =============================================
    
    @staticmethod
    @login_required
    def get_category(category_id):
        """Get category details by ID"""
        try:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'success': False, 'message': 'Category not found'}), 404
            
            # Get parent info
            parent_info = None
            if category.parent_category_id:
                parent = Category.query.get(category.parent_category_id)
                if parent:
                    parent_info = parent.to_dict_minimal()
            
            # Get children count
            children_count = Category.query.filter_by(parent_category_id=category_id).count()
            
            # Get immediate children
            children = Category.query.filter_by(
                parent_category_id=category_id
            ).order_by(Category.display_order).all()
            
            return jsonify({
                'success': True,
                'data': category.to_dict(),
                'parent': parent_info,
                'children_count': children_count,
                'children': [child.to_dict_minimal() for child in children]
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # =============================================
    # UPDATE CATEGORY
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def update_category(category_id):
        """Update an existing category"""
        try:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'success': False, 'message': 'Category not found'}), 404
            
            data = request.get_json()
            
            # Update category name
            if data.get('category_name'):
                if not CategoryController.validate_category_name(data['category_name']):
                    return jsonify({'success': False, 'message': 'Category name must be at least 2 characters'}), 400
                existing = Category.query.filter_by(category_name=data['category_name'].strip()).first()
                if existing and existing.category_id != category_id:
                    return jsonify({'success': False, 'message': 'Category name already exists'}), 400
                category.category_name = data['category_name'].strip()
            
            # Update category code
            if data.get('category_code'):
                if not CategoryController.validate_category_code(data['category_code']):
                    return jsonify({'success': False, 'message': 'Category code must be at least 2 characters and alphanumeric'}), 400
                existing = Category.query.filter_by(category_code=data['category_code'].strip().upper()).first()
                if existing and existing.category_id != category_id:
                    return jsonify({'success': False, 'message': 'Category code already exists'}), 400
                category.category_code = data['category_code'].strip().upper()
            
            # Update description
            if data.get('description') is not None:
                category.description = data['description'].strip() if data['description'] else None
            
            # Update icon
            if data.get('icon') is not None:
                category.icon = data['icon'].strip() if data['icon'] else None
            
            # Update display order
            if data.get('display_order') is not None:
                category.display_order = data['display_order']
            
            # Update status
            if data.get('status'):
                valid_statuses = ['Active', 'Inactive']
                if data['status'] not in valid_statuses:
                    return jsonify({'success': False, 'message': 'Invalid status'}), 400
                category.status = data['status']
            
            # Update parent category
            if 'parent_category_id' in data:
                parent_id = data['parent_category_id']
                
                # If setting to None, make it a root category
                if parent_id is None:
                    category.parent_category_id = None
                else:
                    # Validate parent
                    parent = Category.query.get(parent_id)
                    if not parent:
                        return jsonify({'success': False, 'message': 'Parent category not found'}), 400
                    if parent.status != 'Active':
                        return jsonify({'success': False, 'message': 'Parent category must be active'}), 400
                    # Prevent circular reference
                    if parent_id == category_id:
                        return jsonify({'success': False, 'message': 'Cannot set category as its own parent'}), 400
                    # Prevent deep nesting beyond 3 levels
                    level = CategoryController._get_category_level(parent)
                    if level >= 2:
                        return jsonify({'success': False, 'message': 'Maximum nesting level (3) exceeded'}), 400
                    
                    category.parent_category_id = parent_id
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Category updated successfully',
                'data': category.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @staticmethod
    def _get_category_level(category):
        """Get the level of a category (0 for root)"""
        level = 0
        current = category
        while current.parent_category_id:
            level += 1
            current = Category.query.get(current.parent_category_id)
            if not current:
                break
        return level
    
    # =============================================
    # DELETE CATEGORY
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def delete_category(category_id):
        """Delete a category (soft delete or full delete)"""
        try:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'success': False, 'message': 'Category not found'}), 404
            
            # Check if category has subcategories
            subcategories = Category.query.filter_by(parent_category_id=category_id).all()
            if subcategories:
                return jsonify({
                    'success': False,
                    'message': 'Cannot delete category with subcategories',
                    'subcategories': [sub.to_dict_minimal() for sub in subcategories]
                }), 400
            
            # Check if category has courses
            if category.courses.count() > 0:
                return jsonify({
                    'success': False,
                    'message': 'Cannot delete category with associated courses',
                    'courses': [course.to_dict_minimal() for course in category.courses]
                }), 400
            
            # Soft delete by default (set status to Inactive)
            if request.args.get('permanent', 'false').lower() == 'true':
                # Permanent delete (Admin only)
                if not current_user.is_admin():
                    return jsonify({'success': False, 'message': 'Only admins can permanently delete categories'}), 403
                db.session.delete(category)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Category deleted permanently'}), 200
            else:
                # Soft delete
                category.status = 'Inactive'
                db.session.commit()
                return jsonify({
                    'success': True,
                    'message': 'Category deactivated successfully',
                    'data': category.to_dict_minimal()
                }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # =============================================
    # BULK REORDER CATEGORIES
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def reorder_categories():
        """Bulk reorder categories"""
        try:
            data = request.get_json()
            
            if not data or not isinstance(data, list):
                return jsonify({'success': False, 'message': 'Expected array of category orders'}), 400
            
            categories_data = data.get('categories', [])
            if not categories_data:
                return jsonify({'success': False, 'message': 'No categories provided'}), 400
            
            for item in categories_data:
                if not item.get('category_id') or item.get('display_order') is None:
                    continue
                
                category = Category.query.get(item['category_id'])
                if category:
                    category.display_order = item['display_order']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Categories reordered successfully',
                'updated_count': len(categories_data)
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # =============================================
    # GET CATEGORY HIERARCHY
    # =============================================
    
    @staticmethod
    @login_required
    def get_category_hierarchy():
        """Get full category hierarchy"""
        try:
            root_categories = Category.query.filter(
                Category.parent_category_id.is_(None),
                Category.status == 'Active'
            ).order_by(Category.display_order).all()
            
            hierarchy = []
            for root in root_categories:
                hierarchy.append(CategoryController._build_category_tree(root))
            
            return jsonify({
                'success': True,
                'data': hierarchy
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # =============================================
    # GET CATEGORY STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_category_stats():
        """Get category statistics"""
        try:
            total = Category.query.count()
            active = Category.query.filter_by(status='Active').count()
            inactive = Category.query.filter_by(status='Inactive').count()
            
            # Root categories
            root_categories = Category.query.filter(
                Category.parent_category_id.is_(None)
            ).count()
            
            # Categories with children
            with_children = Category.query.filter(
                Category.category_id.in_(
                    db.session.query(Category.parent_category_id)
                    .filter(Category.parent_category_id.isnot(None))
                )
            ).count()
            
            # Categories without children
            without_children = total - with_children
            
            return jsonify({
                'success': True,
                'data': {
                    'total_categories': total,
                    'active_categories': active,
                    'inactive_categories': inactive,
                    'root_categories': root_categories,
                    'categories_with_children': with_children,
                    'categories_without_children': without_children
                }
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    # =============================================
    # SIMPLE LIST CATEGORIES (For backward compatibility)
    # =============================================
    
    @staticmethod
    @login_required
    def list_categories_simple():
        """Simple list all categories without hierarchy"""
        try:
            search = request.args.get('search', '')
            status = request.args.get('status', '')
            
            query = Category.query
            
            if search:
                query = query.filter(
                    or_(
                        Category.category_name.ilike(f'%{search}%'),
                        Category.category_code.ilike(f'%{search}%')
                    )
                )
            if status and status != '':
                query = query.filter(Category.status == status)
            
            categories = query.order_by(Category.display_order).all()
            
            return jsonify({
                'success': True,
                'data': [c.to_dict() for c in categories]
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
