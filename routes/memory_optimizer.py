# routes/memory_optimizer.py
"""
Omniverse Smart City Platform - Tripoli Node
Dynamic Memory Optimization & Policy-Compliant Resource Controller
Engineered for: Pi Network SDK 2.0 & Autonomous Agents Infrastructure
"""

import gc
import os
import sys
import psutil
from flask import Blueprint, jsonify, request

memory_bp = Blueprint('memory_optimizer', __name__)

# حد التنبيه لاستغلال الذاكرة (80% للحفاظ على استقرار النظام المحلي)
MEMORY_THRESHOLD_PERCENT = 80.0

def force_garbage_collection():
    """تفرغ الذاكرة المهدرة فوراً وبشكل آمن متوافق مع البيئات المستضافة والمحلية"""
    collected = gc.collect()
    return collected

def check_system_memory():
    """فحص سلامة الذاكرة وموارد العقدة"""
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024**3), 2),
        "available_gb": round(mem.available / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "percent_used": mem.percent
    }

@memory_bp.route('/api/v1/memory/status', methods=['GET'])
def get_memory_status():
    """مسار للتحقق من حالة الذاكرة في عقدة طرابلس"""
    status = check_system_memory()
    is_critical = status['percent_used'] > MEMORY_THRESHOLD_PERCENT
    
    if is_critical:
        # استدعاء تنظيف إجباري في حال تجاوز الحد
        force_garbage_collection()
    
    return jsonify({
        "status": "success",
        "node": "Tripoli_Node_v0.6.3",
        "memory": status,
        "optimization_active": True,
        "warning": "High memory usage detected, cache purged." if is_critical else "Memory operating within safe boundaries."
    }), 200

@memory_bp.route('/api/v1/memory/purge', methods=['POST'])
def purge_memory():
    """مسار يدوي لتفريغ الذاكرة المؤقتة للوكلاء الذكيين"""
    freed_objects = force_garbage_collection()
    updated_status = check_system_memory()
    
    return jsonify({
        "status": "success",
        "message": "Memory purged successfully.",
        "freed_objects_count": freed_objects,
        "current_available_ram_gb": updated_status['available_gb']
    }), 200