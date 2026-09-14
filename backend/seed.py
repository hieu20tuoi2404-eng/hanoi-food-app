"""Seed 30 demo Hanoi dishes with restaurants, recipes, and reviews.

All data is marked as Demo / Chưa xác minh.
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timedelta

import database as db

DISHES: list[dict] = [
    # ================= BỮA SÁNG (10) =================
    {
        "name": "Phở bò Hà Nội",
        "slug": "pho-bo-ha-noi",
        "description": "Phở bò truyền thống nước dùng trong, ngọt thanh từ xương, thịt bò tái/nạm/tái chín",
        "meal_type": "breakfast",
        "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 9,
        "avg_price": 50000,
        "restaurants": [
            {"name": "Phở Gia Truyền", "address": "49 Bát Đàn", "district": "Hoàn Kiếm", "hours": "06:00-10:00", "price_range": "40.000-60.000đ"},
            {"name": "Phở Thìn", "address": "13 Lò Đúc", "district": "Hai Bà Trưng", "hours": "06:00-08:30", "price_range": "50.000-70.000đ"},
        ],
        "recipe": {
            "ingredients": ["Xương bò 1kg", "Bánh phở tươi 500g", "Hành tây 2 củ", "Gừng 1 nhánh", "Quế 1 thanh", "Hạt ngò 1 thìa", "Nước mắm 3 thìa", "Muối"],
            "portions": "4-5 bát",
            "cook_time": "4-5 tiếng (nước dùng)",
            "steps": [
                "Luộc xương 2 lần, rửa sạch lần cuối",
                "Ninh xương với gừng đập dập + hành tây nướng + quế + hạt ngò",
                "Đun sôi vặn nhỏ 3-4 tiếng, hớt bọt liên tục",
                "Nêm nước mắm + muối vừa miệng",
                "Chần phở, xếp thịt lên, chan nước dùng nóng",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 9, "comment": "Nước dùng ngọt thanh, thịt tươi. Phải xếp hàng sáng sớm mới được.", "reviewer_name": "Minh Anh"},
            {"rating": 8, "comment": "Quán cũ, sạch sẽ, phở đúng vị Hà Nội.", "reviewer_name": "Hà Linh"},
        ],
    },
    {
        "name": "Bún chả",
        "slug": "bun-cha",
        "description": "Bún chả than hoa thịt nướng mỡ chả, chấm nước mắm chua ngọt, ăn kèm rau sống",
        "meal_type": "breakfast",
        "image_url": "https://images.unsplash.com/photo-1583224994076-089a0fb08c24?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 9,
        "avg_price": 45000,
        "restaurants": [
            {"name": "Bún Chả Hương Liên", "address": "24 Lê Văn Hưu", "district": "Hoàn Kiếm", "hours": "10:00-14:00", "price_range": "40.000-55.000đ"},
            {"name": "Bún Chả Đắc Kim", "address": "1 Hàng Mành", "district": "Hoàn Kiếm", "hours": "11:00-14:00", "price_range": "45.000-60.000đ"},
        ],
        "recipe": {
            "ingredients": ["Thịt ba chỉ 500g", "Chả meat 300g", "Bún tươi 300g", "Nước mắm", "Đường", "Giấm", "Tỏi", "Ớt", "Rau sống"],
            "portions": "2-3 người",
            "cook_time": "45 phút",
            "steps": [
                "Thái thịt mỏng, ướp nước mắm + đường + tỏi 30 phút",
                "Làm chả: thịt xay ướp gia vị, nặn viên nhỏ",
                "Nướng thịt + chả trên than hoa",
                "Pha nước chấm: nước mắm + đường + giấm + tỏi ớt",
                "Bày bún + thịt nướng + chả + rau sống, chan nước chấm",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 9, "comment": "Bún chả Obama ăn hồi nào vẫn ngon. Thịt nướng than hoa thơm.", "reviewer_name": "Tuấn Anh"},
            {"rating": 8, "comment": "Chả nướng thơm, nước chấm vừa miệng.", "reviewer_name": "Mai Linh"},
        ],
    },
    {
        "name": "Bánh cuốn",
        "slug": "banh-cuon",
        "description": "Bánh cuốn mỏng mềm nhân thịt băm + mộc nhĩ, chấm nước mắm chua ngọt",
        "meal_type": "breakfast",
        "image_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 30000,
        "restaurants": [
            {"name": "Bánh Cuốn Bà Hanh", "address": "26 Thọ Xương", "district": "Hoàn Kiếm", "hours": "06:30-11:00", "price_range": "25.000-35.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bột gạo 200g", "Thịt băm 150g", "Mộc nhĩ khô 30g", "Hành khô", "Nước mắm", "Giấm"],
            "portions": "2 người",
            "cook_time": "30 phút",
            "steps": [
                "Ngâm mộc nhĩ, thái nhỏ, xào cùng thịt băm + hành khô",
                "Pha bột: bột gạo + nước + dầu ăn, khuấy đều",
                "Tráng bánh mỏng trên nồi hấp",
                "Nhân lên, cuốn lại, xếp ra đĩa",
                "Pha nước chấm, rắc hành phi",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Bánh mỏng, nhân đầy, nước chấm ngon.", "reviewer_name": "Quỳnh Chi"},
        ],
    },
    {
        "name": "Xôi xéo",
        "slug": "xoi-xeo",
        "description": "Xôi đậu xanh dẻo thơm, ăn kèm hành phi, ruốc, giò lụa",
        "meal_type": "breakfast",
        "image_url": "https://images.unsplash.com/photo-1569058242253-92a9c755a0ec?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 25000,
        "restaurants": [
            {"name": "Xôi Yến", "address": "35B Nguyễn Hữu Huân", "district": "Hoàn Kiếm", "hours": "05:00-12:00", "price_range": "20.000-40.000đ"},
        ],
        "recipe": {
            "ingredients": ["Gạo nếp 300g", "Đậu xanh cà vỏ 200g", "Hành khô", "Dầu ăn", "Muối"],
            "portions": "3-4 người",
            "cook_time": "2 tiếng",
            "steps": [
                "Ngâm nếp + đậu xanh qua đêm",
                "Hấp đậu xanh chín, tán mịn, nặn viên",
                "Trộn nếp + đậu xanh + dầu + muối, đồ chín",
                "Phi hành khô vàng giòn",
                "Múc xôi ra đĩa, rắc hành phi, ăn kèm giò",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Xôi dẻo, đậu xanh mịn. Quán mở sớm, rất tiện.", "reviewer_name": "Hồng Nhung"},
        ],
    },
    {
        "name": "Bánh mì patê",
        "slug": "banh-mi-pate",
        "description": "Bánh mì giòn nhân patê bơ, thịt nguội, dưa chua, rau sống",
        "meal_type": "breakfast",
        "image_url": "https://images.unsplash.com/photo-1558030006-450675393462?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 25000,
        "restaurants": [
            {"name": "Bánh Mì 25", "address": "25 Hàng Cá", "district": "Hoàn Kiếm", "hours": "06:00-21:00", "price_range": "20.000-35.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bánh mì dài", "Patê", "Thịt nguội", "Pơ lai", "Dưa chuột", "Rau sống", "Xốt ớt"],
            "portions": "1 người",
            "cook_time": "10 phút",
            "steps": [
                "Cắt bánh mì, phết patê + bơ",
                "Cho thịt nguội, dưa chua, rau sống",
                "Thêm xốt ớt tùy khẩu vị",
                "Đóng lại, thưởng thức nóng",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Bánh giòn, nhân đầy, giá rẻ.", "reviewer_name": "Đức Minh"},
        ],
    },
    {
        "name": "Phở gà",
        "slug": "pho-ga",
        "description": "Phở gà ta nước dùng trong, thịt gà luộc mềm, da giòn",
        "meal_type": "breakfast",
        "image_url": "https://images.unsplash.com/photo-1512003867073-a4bf461a1e5f?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 45000,
        "restaurants": [
            {"name": "Phở Gà Thìn Bờ Hồ", "address": "61 Đinh Tiên Hoàng", "district": "Hoàn Kiếm", "hours": "06:00-10:00", "price_range": "40.000-55.000đ"},
        ],
        "recipe": {
            "ingredients": ["Gà ta 1 con", "Bánh phở", "Gừng", "Hành tây", "Nước mắm", "Muối", "Rau mùi"],
            "portions": "4 người",
            "cook_time": "1 tiếng",
            "steps": [
                "Luộc gà với gừng + hành tây, vớt ra",
                "Ninh nước dùng gà thêm 30 phút",
                "Thái gà bày lên bát",
                "Chần phở, chan nước dùng nóng",
                "Rắc hành ngò, thêm chanh ớt",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Phở gà thanh, da gà giòn ngon.", "reviewer_name": "Thanh Hương"},
        ],
    },
    {
        "name": "Cháo sườn",
        "slug": "chao-suon",
        "description": "Cháo gạo tẻ mịn, sườn non hầm mềm, ăn kèm quẩy giòn",
        "meal_type": "breakfast",
        "image_url": "https://images.unsplash.com/photo-1603105037880-880cd4f7e099?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 7,
        "avg_price": 30000,
        "restaurants": [
            {"name": "Cháo Sườn Sụn Cây Bàng", "address": "27 Hàng Bún", "district": "Hoàn Kiếm", "hours": "06:00-10:30", "price_range": "25.000-35.000đ"},
        ],
        "recipe": {
            "ingredients": ["Gạo tẻ 150g", "Sườn non 300g", "Gừng", "Muối", "Tiêu", "Quẩy"],
            "portions": "2 người",
            "cook_time": "1 tiếng 30 phút",
            "steps": [
                "Vo gạo, ngâm 30 phút",
                "Luộc sườn, lấy nước dùng",
                "Ninh gạo với nước sườn đến khi nhuyễn",
                "Thêm sườn vào, nêm gia vị",
                "Múc ra bát, ăn kèm quẩy",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 7, "comment": "Cháo mịn, sườn mềm, quẩy giòn.", "reviewer_name": "Ngọc Ánh"},
        ],
    },
    {
        "name": "Bánh bao",
        "slug": "banh-bao",
        "description": "Bánh bao nhân thịt mộc nhĩ, trứng cút, bột mềm xốp",
        "meal_type": "breakfast",
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 7,
        "avg_price": 15000,
        "restaurants": [
            {"name": "Bánh Bao Cô Lan", "address": "38 Hàng Điếu", "district": "Hoàn Kiếm", "hours": "06:00-18:00", "price_range": "12.000-18.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bột bánh bao 300g", "Thịt xay 200g", "Mộc nhĩ", "Trứng cút luộc", "Nấm hương"],
            "portions": "8-10 bánh",
            "cook_time": "45 phút",
            "steps": [
                "Trộn bột với men + đường + sữa, để nở 1 tiếng",
                "Làm nhân: thịt + mộc nhĩ + nấm + trứng cút",
                "Nhào bột, chia nhỏ, cán mỏng",
                "Đặt nhân vào, bọc lại",
                "Hấp 20 phút đến khi chín",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 7, "comment": "Bánh mềm, nhân đầy. Mua về ăn sáng tiện.", "reviewer_name": "Văn Đức"},
        ],
    },
    {
        "name": "Mì vằn thắn",
        "slug": "mi-van-than",
        "description": "Mì vằn thắn sợi mì vàng, nước dùng trong, nhân tôm thịt mộc nhĩ",
        "meal_type": "breakfast",
        "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 40000,
        "restaurants": [
            {"name": "Mì Vằn Thắn Thọ Xương", "address": "7 Thọ Xương", "district": "Hoàn Kiếm", "hours": "06:30-11:00", "price_range": "35.000-45.000đ"},
        ],
        "recipe": {
            "ingredients": ["Mì tươi 200g", "Tôm 150g", "Thịt nạc 150g", "Mộc nhĩ", "Xương ống", "Gừng"],
            "portions": "2 người",
            "cook_time": "1 tiếng",
            "steps": [
                "Ninh nước dùng xương + gừng",
                "Làm nhân tôm thịt: băm nhuyễn, trộn gia vị",
                "Hấp nhân chín, thái mỏng",
                "Trần mì, bày nhân lên",
                "Chan nước dùng nóng",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Nước dùng trong, nhân ngon, sợi mì dai.", "reviewer_name": "Bảo Châu"},
        ],
    },
    {
        "name": "Cốm làng Vòng",
        "slug": "com-lang-vong",
        "description": "Cốm xanh dẻo thơm, cuộn lá sen, thường bán theo mùa thu",
        "meal_type": "breakfast",
        "image_url": "https://images.unsplash.com/photo-1606731219412-fb38b0cbe6de?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 40000,
        "restaurants": [
            {"name": "Cốm Làng Vòng", "address": "Ngã tư Lê Văn Lương - Trần Duy Hưng", "district": "Cầu Giấy", "hours": "Tháng 9-11 âm lịch", "price_range": "35.000-50.000đ/lon"},
        ],
        "recipe": {
            "ingredients": ["Cốm tươi 200g", "Đậu xanh", "Dừa nạo", "Đường", "Bột sắn"],
            "portions": "2-3 người",
            "cook_time": "30 phút",
            "steps": [
                "Làm nhân: đậu xanh + dừa + đường, xào khô",
                "Nắn cốm nhỏ, trộn đường",
                "Cốm ra lá sen, cho nhân vào",
                "Cuộn chặt lại",
                "Ăn ngay hoặc hấp lại",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Cốm dẻo thơm đúng vị Hà Nội. Chỉ bán mùa thu.", "reviewer_name": "Thúy Hà"},
        ],
    },

    # ================= BỮA TRƯA (8) =================
    {
        "name": "Bún bò Nam Bộ",
        "slug": "bun-bo-nam-bo",
        "description": "Bún bò xào tái chan nước mắm chua ngọt, đậu phộng rang, rau sống",
        "meal_type": "lunch",
        "image_url": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 45000,
        "restaurants": [
            {"name": "Bún Bò Nam Bộ 67 Hàng Điếu", "address": "67 Hàng Điếu", "district": "Hoàn Kiếm", "hours": "10:00-14:00", "price_range": "40.000-50.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bún tươi 200g", "Thịt bò 200g", "Đậu phộng", "Rau sống", "Nước mắm", "Đường", "Giấm"],
            "portions": "1-2 người",
            "cook_time": "25 phút",
            "steps": [
                "Thái bò mỏng, ướp nước mắm + tỏi",
                "Xào bò tái nhanh trên lửa lớn",
                "Pha nước chấm: nước mắm + đường + giấm + tỏi ớt",
                "Bày bún + bò xào + đậu phộng rang",
                "Chan nước chấm, thêm rau sống",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Bún bò tái chan ngon, đậu phộng giòn.", "reviewer_name": "Thùy Dung"},
        ],
    },
    {
        "name": "Cơm tấm sườn nướng",
        "slug": "com-tam-suon-nuong",
        "description": "Cơm tấm sườn nướng bì chả, nước chấm chua ngọt, dưa chua",
        "meal_type": "lunch",
        "image_url": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 50000,
        "restaurants": [
            {"name": "Cơm Tấm Phúc", "address": "28 Hàng Tre", "district": "Hoàn Kiếm", "hours": "10:00-14:00 & 17:00-21:00", "price_range": "40.000-60.000đ"},
        ],
        "recipe": {
            "ingredients": ["Gạo tấm 300g", "Sườn non 300g", "Bì heo", "Trứng gà", "Nước mắm", "Đường"],
            "portions": "2 người",
            "cook_time": "45 phút",
            "steps": [
                "Nấu cơm tấm mềm",
                "Ướp sườn với ngũ vị hương + đường, nướng",
                "Làm bì: thịt heo luộc thái sợi + bì heo",
                "Pha nước chấm",
                "Bày cơm + sườn nướng + bì + trứng",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Sườn nướng thơm, cơm tấm dẻo. Quán nhỏ đông khách.", "reviewer_name": "Hải Nam"},
        ],
    },
    {
        "name": "Bún ốc",
        "slug": "bun-oc",
        "description": "Bún ốc nước dùng chua cà chua, ốc dai giòn, đậu phụ chiên",
        "meal_type": "lunch",
        "image_url": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 40000,
        "restaurants": [
            {"name": "Bún Ốc Cô Hạnh", "address": "23 Hàng Chai", "district": "Hoàn Kiếm", "hours": "10:00-14:00", "price_range": "35.000-45.000đ"},
        ],
        "recipe": {
            "ingredients": ["Ốc vú 400g", "Bún tươi", "Cà chua", "Me", "Đậu phụ", "Hành lá", "Tía tô"],
            "portions": "2 người",
            "cook_time": "40 phút",
            "steps": [
                "Luộc ốc, lấy thịt, giữ nước luộc",
                "Xào cà chua + me, cho nước luộc ốc vào",
                "Nấu sôi, thêm đậu phụ chiên",
                "Trần bún, chan nước ốc nóng",
                "Rắc hành lá + tía tô",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Nước dùng chua thanh, ốc giòn.", "reviewer_name": "Kim Ngọc"},
        ],
    },
    {
        "name": "Bánh đa cua",
        "slug": "banh-da-cua",
        "description": "Bánh đa đỏ cua bể, nước dùng ngọt từ cua, rau muống chẻ",
        "meal_type": "lunch",
        "image_url": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 45000,
        "restaurants": [
            {"name": "Bánh Đa Cua Hàng Kênh", "address": "35 Hàng Kênh", "district": "Hoàn Kiếm", "hours": "10:00-14:00", "price_range": "40.000-55.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bánh đa đỏ 200g", "Cua bể 500g", "Rau muống", "Hành khô", "Gừng"],
            "portions": "2 người",
            "cook_time": "45 phút",
            "steps": [
                "Cua hấp chín, gạch cua để riêng",
                "Ninh nước dùng từ gạch cua + gừng",
                "Trần bánh đa, xếp rau muống chẻ",
                "Chan nước dùng cua nóng",
                "Thêm gạch cua lên trên",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Nước dùng cua ngọt tự nhiên, bánh đa mềm.", "reviewer_name": "Ngọc Lan"},
        ],
    },
    {
        "name": "Nem chua rán",
        "slug": "nem-chua-ran",
        "description": "Nem chua rán vàng giòn, chấm tương ớt, ăn kèm rau sống",
        "meal_type": "lunch",
        "image_url": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 35000,
        "restaurants": [
            {"name": "Nem Rán Bà Phượng", "address": "16 Hàng Bông", "district": "Hoàn Kiếm", "hours": "10:00-22:00", "price_range": "30.000-45.000đ"},
        ],
        "recipe": {
            "ingredients": ["Thịt lợn xay 300g", "Bì heo", "Nước mắm", "Đường", "Bột chiên giòn", "Dầu ăn"],
            "portions": "2 người",
            "cook_time": "30 phút",
            "steps": [
                "Trộn thịt xay + bì thái sợi + gia vị",
                "Nặn viên, lăn bột chiên giòn",
                "Chiên vàng giòn trong dầu nóng",
                "Vớt ra giấy thấm dầu",
                "Ăn kèm tương ớt + rau sống",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Nem giòn, nhân chua vừa miệng.", "reviewer_name": "Quốc Bảo"},
        ],
    },
    {
        "name": "Phở xào",
        "slug": "pho-xao",
        "description": "Phở xào thịt bò rau cải, sợi phở dai thấm vị tương đen",
        "meal_type": "lunch",
        "image_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 7,
        "avg_price": 50000,
        "restaurants": [
            {"name": "Phở Xào 88 Hàng Đậu", "address": "88 Hàng Đậu", "district": "Hoàn Kiếm", "hours": "10:00-14:00", "price_range": "45.000-55.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bánh phở tươi 250g", "Thịt bò 200g", "Rau cải", "Tương đen", "Dầu hào", "Tỏi"],
            "portions": "1-2 người",
            "cook_time": "20 phút",
            "steps": [
                "Thái bò mỏng, ướp dầu hào + tỏi",
                "Xào bò tái, để riêng",
                "Xào rau cải + tương đen",
                "Thêm phở + bò vào, đảo đều",
                "Ăn nóng ngay",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 7, "comment": "Phở dai, bò mềm. Không gian nhỏ.", "reviewer_name": "Minh Tuấn"},
        ],
    },
    {
        "name": "Chả cá Lã Vọng",
        "slug": "cha-ca-la-vong",
        "description": "Chả cá chiên vàng mềm, cá Basa ướp nghệ + thì là, ăn kèm bún + nước mắm",
        "meal_type": "lunch",
        "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 9,
        "avg_price": 120000,
        "restaurants": [
            {"name": "Chả Cá Lã Vọng", "address": "14 Chả Cá", "district": "Hoàn Kiếm", "hours": "11:00-14:00 & 17:00-21:00", "price_range": "100.000-150.000đ"},
        ],
        "recipe": {
            "ingredients": ["Cá Basa phi lê 500g", "Nghệ tươi", "Thì là", "Mẻ", "Bún tươi", "Đậu phộng", "Nước mắm"],
            "portions": "2-3 người",
            "cook_time": "40 phút",
            "steps": [
                "Cá cắt khúc, ướp nghệ + mẻ + thì là 30 phút",
                "Chiên cá vàng đều hai mặt",
                "Bày bún + cá + đậu phộng rang + thì là",
                "Pha nước mắm chua ngọt",
                "Ăn nóng ngay trên chảo",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 9, "comment": "Đúng vị truyền thống, cá thơm. Giá cao nhưng xứng.", "reviewer_name": "Thanh Thảo"},
            {"rating": 8, "comment": "Lần đầu ăn, ấn tượng. Không gian cổ kính.", "reviewer_name": "Duy Khánh"},
        ],
    },
    {
        "name": "Bún thang",
        "slug": "bun-thang",
        "description": "Bún thang nước dùng gà trong, thịt gà xé + trứng thái sợi + hành khô",
        "meal_type": "lunch",
        "image_url": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 45000,
        "restaurants": [
            {"name": "Bún Thang Bà Đức", "address": "48 Hàng Quạt", "district": "Hoàn Kiếm", "hours": "06:30-11:00", "price_range": "40.000-50.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bún tươi 200g", "Gà ta 300g", "Trứng gà", "Hành khô", "Nước mắm", "Rau mùi"],
            "portions": "2 người",
            "cook_time": "1 tiếng",
            "steps": [
                "Luộc gà, thái sợi + trứng chiên thái sợi",
                "Ninh nước dùng gà",
                "Pha nước mắm + giấm + đường",
                "Trần bún, xếp gà + trứng + hành khô",
                "Chan nước dùng nóng, rắc rau mùi",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Nước dùng thanh, trình bày đẹp mắt.", "reviewer_name": "Phương Anh"},
        ],
    },

    # ================= BỮA TỐI (6) =================
    {
        "name": "Lẩu bò nhúng mẻ",
        "slug": "lau-bo-nhung-me",
        "description": "Lẩu bò nhúng mẻ chua ngọt, thịt bò tươi nhúng nước dùng sôi",
        "meal_type": "dinner",
        "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 200000,
        "restaurants": [
            {"name": "Lẩu Bò Nhúng Mẻ 34 Hàng Tre", "address": "34 Hàng Tre", "district": "Hoàn Kiếm", "hours": "17:00-22:00", "price_range": "150.000-250.000đ"},
        ],
        "recipe": {
            "ingredients": ["Thịt bò phi lê 500g", "Mẻ 200g", "Rau cải", "Đậu phụ", "Nấm kim châm", "Bún", "Bún tàu"],
            "portions": "3-4 người",
            "cook_time": "30 phút chuẩn bị",
            "steps": [
                "Pha nước lẩu: mẻ + nước dùng + nấm",
                "Đun sôi nồi lẩu",
                "Thái bò mỏng, bày ra đĩa",
                "Nhúng bò vào lẩu 3-5 giây",
                "Ăn kèm bún + rau sống",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Lẩu chua thanh, thịt bò tươi nhúng mềm.", "reviewer_name": "Thanh Hằng"},
        ],
    },
    {
        "name": "Nướng BBQ",
        "slug": "nuong-bbq",
        "description": "Tiệc nướng với thịt bò, tôm, mực, rau củ nướng than hoa",
        "meal_type": "dinner",
        "image_url": "https://images.unsplash.com/photo-1558030137-a56c1b004fa3?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 7,
        "avg_price": 180000,
        "restaurants": [
            {"name": "Vườn Nướng Thả Ga", "address": "Khu đô thị sinh thái Tây Hồ Tây", "district": "Tây Hồ", "hours": "10:00-22:00", "price_range": "150.000-250.000đ/người"},
        ],
        "recipe": {
            "ingredients": ["Thịt bò 500g", "Tôm 300g", "Mực 200g", "Rau củ", "Nước mắm + đường + tỏi (ướp)", "Than hoa"],
            "portions": "4-6 người",
            "cook_time": "1 tiếng",
            "steps": [
                "Ướp thịt + tôm + mực riêng",
                "Chuẩn bị vỉ nướng + than hoa",
                "Nướng thịt trước, sau đó tôm mực",
                "Nướng rau củ kèm theo",
                "Chấm nước mắm pha",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 7, "comment": "Không gian đẹp, thịt tươi. BBQ phù hợp nhóm đông.", "reviewer_name": "Ngọc Huyền"},
        ],
    },
    {
        "name": "Bún riêu cua",
        "slug": "bun-rieu-cua",
        "description": "Bún riêu cua ốc chua cay, cà chua, đậu phụ, rau muống chẻ",
        "meal_type": "dinner",
        "image_url": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 40000,
        "restaurants": [
            {"name": "Bún Riêu Cua 34 Hàng Bông", "address": "34 Hàng Bông", "district": "Hoàn Kiếm", "hours": "10:00-21:00", "price_range": "35.000-45.000đ"},
        ],
        "recipe": {
            "ingredients": ["Cua đồng 400g", "Bún tươi", "Cà chua", "Me", "Đậu phụ", "Rau muống"],
            "portions": "2 người",
            "cook_time": "45 phút",
            "steps": [
                "Cua giã nhỏ, lọc lấy nước gạch",
                "Xào cà chua + me",
                "Cho nước gạch cua vào, đun sôi",
                "Thêm đậu phụ chiên",
                "Chan bún + rau sống",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Riêu cua béo ngậy, chua cay vừa.", "reviewer_name": "Hạnh Nguyên"},
        ],
    },
    {
        "name": "Vịt quay",
        "slug": "vit-quay",
        "description": "Vịt quay da giòn thịt mềm, ướp ngũ vị hương, ăn kèm tương xì dầu",
        "meal_type": "dinner",
        "image_url": "https://images.unsplash.com/photo-1518492104633-130d0cc84637?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 150000,
        "restaurants": [
            {"name": "Vịt Quay Vân Đình", "address": "88 Hàng Gai", "district": "Hoàn Kiếm", "hours": "16:00-22:00", "price_range": "130.000-180.000đ/con"},
        ],
        "recipe": {
            "ingredients": ["Vịt 1 con (~1.5kg)", "Ngũ vị hương", "Mật ong", "Nước tương", "Gừng", "Hành tây"],
            "portions": "3-4 người",
            "cook_time": "2 tiếng",
            "steps": [
                "Vịt rửa sạch, chần nước sôi",
                "Ướp ngũ vị hương + mật ong + nước tương",
                "Phơi khô da 30 phút",
                "Quay ở 180°C trong 1 tiếng, lật mặt",
                "Thái miếng, ăn kèm tương",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Da giòn, thịt mềm, ướp thấm.", "reviewer_name": "Hoàng Dũng"},
        ],
    },
    {
        "name": "Thịt kho trứng vịt",
        "slug": "thit-kho-trung-vit",
        "description": "Thịt kho mắm ruốc trứng vịt, nước kho sánh mặn ngọt, ăn cơm nóng",
        "meal_type": "dinner",
        "image_url": "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 7,
        "avg_price": 60000,
        "restaurants": [
            {"name": "Quán Cơm Nhà 63 Hàng Bông", "address": "63 Hàng Bông", "district": "Hoàn Kiếm", "hours": "10:00-14:00 & 17:00-21:00", "price_range": "50.000-70.000đ"},
        ],
        "recipe": {
            "ingredients": ["Thịt ba chỉ 400g", "Trứng gà hoặc trứng vịt luộc", "Nước mắm", "Đường", "Nước dừa", "Hành tím"],
            "portions": "2-3 người",
            "cook_time": "1 tiếng",
            "steps": [
                "Thái thịt, chần nước sôi",
                "Phi hành tím, xào thịt với đường (đường phèn)",
                "Cho nước mắm + nước dừa vào, đun sôi",
                "Thêm trứng, kho nhỏ lửa 45 phút",
                "Nước kho sánh, nêm vừa miệng",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 7, "comment": "Món kho quen thuộc, ăn cơm nóng ngon.", "reviewer_name": "Bích Liên"},
        ],
    },
    {
        "name": "Chả giò tôm",
        "slug": "cha-gio-tom",
        "description": "Chả giò nhân thịt + tôm + miến + nấm, chiên giòn, chấm nước mắm chua",
        "meal_type": "dinner",
        "image_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 7,
        "avg_price": 50000,
        "restaurants": [
            {"name": "Chả Giò Bà Tuyết", "address": "22 Hàng Bạc", "district": "Hoàn Kiếm", "hours": "10:00-21:00", "price_range": "45.000-55.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bánh tráng", "Thịt xay 200g", "Tôm băm 100g", "Miến", "Nấm hương", "Cà rốt", "Nước mắm"],
            "portions": "2 người",
            "cook_time": "30 phút",
            "steps": [
                "Ngâm miến + nấm, thái nhỏ",
                "Trộn nhân: thịt + tôm + miến + nấm + cà rốt",
                "Cuộn bánh tráng chặt",
                "Chiên vàng giòn",
                "Chấm nước mắm chua ngọt",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 7, "comment": "Chả giòn, nhân đầy, nước chấm ngon.", "reviewer_name": "Mai Phương"},
        ],
    },

    # ================= ĂN VẶT (6) =================
    {
        "name": "Bánh gối",
        "slug": "banh-goi",
        "description": "Bánh gối nhân thịt + miến + mộc nhĩ, chiên vàng giòn",
        "meal_type": "snack",
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 10000,
        "restaurants": [
            {"name": "Bánh Gối 5 Hàng Chiếu", "address": "5 Hàng Chiếu", "district": "Hoàn Kiếm", "hours": "14:00-22:00", "price_range": "8.000-12.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bột bánh gối", "Thịt xay", "Miến", "Mộc nhĩ", "Trứng cút", "Dầu ăn"],
            "portions": "6-8 bánh",
            "cook_time": "30 phút",
            "steps": [
                "Làm nhân: thịt + miến + mộc nhĩ + trứng cút",
                "Cán bột, cắt hình tròn",
                "Đặt nhân, bọc lại, dùng nĩa ép chặt",
                "Chiên vàng giòn",
                "Ăn kèm tương ớt",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Bánh giòn rụm, nhân đầy. Giá rẻ.", "reviewer_name": "Văn Hùng"},
        ],
    },
    {
        "name": "Trứng vịt lộn",
        "slug": "trung-vit-lon",
        "description": "Trứng vịt lộn luộc chín, rau răm + muối tiêu chanh",
        "meal_type": "snack",
        "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 7,
        "avg_price": 8000,
        "restaurants": [
            {"name": "Quán Trứng Lộn 14 Hàng Bông", "address": "14 Hàng Bông", "district": "Hoàn Kiếm", "hours": "14:00-23:00", "price_range": "7.000-10.000đ/quả"},
        ],
        "recipe": {
            "ingredients": ["Trứng vịt lộn", "Rau răm", "Muối", "Tiêu", "Chanh"],
            "portions": "2 quả/người",
            "cook_time": "15 phút",
            "steps": [
                "Luộc trứng lộn 12-15 phút",
                "Vớt ra, bóc vỏ",
                "Ăn kèm rau răm + muối tiêu chanh",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 7, "comment": "Trứng béo, rau răm cay nồng. Thích hợp ăn chiều tối.", "reviewer_name": "Thanh Tùng"},
        ],
    },
    {
        "name": "Bánh tráng trộn",
        "slug": "banh-trang-tron",
        "description": "Bánh tráng cắt sợi trộn xoài + trứng cút + đậu phộng + rau răm",
        "meal_type": "snack",
        "image_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 20000,
        "restaurants": [
            {"name": "Bánh Tráng Trộn Bà Tuyết", "address": "Phố đi bộ Hồ Gươm", "district": "Hoàn Kiếm", "hours": "16:00-22:00", "price_range": "15.000-25.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bánh tráng", "Xoài xanh", "Trứng cút luộc", "Đậu phộng", "Rau răm", "Nước mắm", "Sa tế"],
            "portions": "1-2 người",
            "cook_time": "15 phút",
            "steps": [
                "Cắt bánh tráng sợi nhỏ",
                "Xoài bào sợi, trứng cút cắt đôi",
                "Trộn tất cả với nước mắm + sa tế",
                "Thêm đậu phộng rang + rau răm",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Chua cay mặn ngọt đủ vị. Snack vỉa hè yêu thích.", "reviewer_name": "Thu Hằng"},
        ],
    },
    {
        "name": "Xôi xéo vỉa hè",
        "slug": "xoi-xeo-via-he",
        "description": "Xôi xéo phần nhỏ ăn vặt, hành phi + ruốc + dưa chuột",
        "meal_type": "snack",
        "image_url": "https://images.unsplash.com/photo-1569058242253-92a9c755a0ec?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 7,
        "avg_price": 15000,
        "restaurants": [
            {"name": "Xôi Yến - Chi nhánh vỉa hè", "address": "Góc Nguyễn Hữu Huân - Lý Thái Tổ", "district": "Hoàn Kiếm", "hours": "06:00-12:00", "price_range": "10.000-20.000đ"},
        ],
        "recipe": {
            "ingredients": ["Xôi xéo (xem công thức xôi xéo)", "Hành phi", "Ruốc thịt", "Dưa chuột"],
            "portions": "1 phần",
            "cook_time": "5 phút (đã có xôi sẵn)",
            "steps": [
                "Múc xôi xéo ra giấy gói",
                "Rắc hành phi + ruốc",
                "Ăn kèm dưa chuột",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 7, "comment": "Tiện, nhanh, no. Phù hợp ăn vặt.", "reviewer_name": "Quốc Anh"},
        ],
    },
    {
        "name": "Nem chua Thanh Hóa",
        "slug": "nem-chua-thanh-hoa",
        "description": "Nem chua lên men tự nhiên, thịt heo lên men chua ngọt",
        "meal_type": "snack",
        "image_url": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 8,
        "avg_price": 20000,
        "restaurants": [
            {"name": "Nem Chua Thanh Hóa 36 Hàng Bông", "address": "36 Hàng Bông", "district": "Hoàn Kiếm", "hours": "09:00-21:00", "price_range": "15.000-25.000đ/cặp"},
        ],
        "recipe": {
            "ingredients": ["Thịt heo nạc 300g", "Bì heo", "Đường", "Muối", "Tỏi", "Ớt", "Lá chuối"],
            "portions": "6-8 gói",
            "cook_time": "2 ngày (lên men)",
            "steps": [
                "Thái thịt mỏng, trộn gia vị + bì",
                "Cuộn lá chuối chặt tay",
                "Để nơi khô thoáng 2 ngày",
                "Khi nem có vị chua là được",
                "Ăn kèm tỏi ớt",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 8, "comment": "Nem chua đúng vị, mua về làm quà ngon.", "reviewer_name": "Dương Hà"},
        ],
    },
    {
        "name": "Bánh rán",
        "slug": "banh-ran",
        "description": "Bánh rán đường vàng giòn, nhân đậu xanh dẻo, phủ mè",
        "meal_type": "snack",
        "image_url": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600",
        "image_source": "https://unsplash.com (Demo - Chưa xác minh)",
        "avg_rating": 7,
        "avg_price": 5000,
        "restaurants": [
            {"name": "Bánh Rán Bọc Đường 12 Hàng Bạc", "address": "12 Hàng Bạc", "district": "Hoàn Kiếm", "hours": "14:00-22:00", "price_range": "4.000-6.000đ"},
        ],
        "recipe": {
            "ingredients": ["Bột nếp 200g", "Đậu xanh", "Đường", "Mè", "Dầu ăn"],
            "portions": "8-10 bánh",
            "cook_time": "30 phút",
            "steps": [
                "Nhào bột nếp + nước ấm",
                "Làm nhân đậu xanh + đường",
                "Nhân vào bột, vo tròn",
                "Lăn mè, chiên vàng",
                "Vớt ra giấy thấm dầu",
            ],
            "source": "Demo - Công thức tổng hợp, chưa xác minh",
        },
        "reviews": [
            {"rating": 7, "comment": "Bánh giòn, nhân dẻo. Đồ ăn vặt quen thuộc.", "reviewer_name": "Thủy Tiên"},
        ],
    },
]


def build_maps_link(name: str, address: str) -> str:
    """Build a Google Maps search URL per the required format."""
    query = f"{name}, {address}, Hà Nội"
    encoded = query.replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&query={encoded}"


def normalize_images() -> None:
    """Point all dishes to locally generated SVG illustrations.

    Images live in frontend/public/images and are served at /images/<slug>.svg.
    image_source is updated to reflect that this is our own demo artwork.
    """
    for dish in DISHES:
        dish["image_url"] = f"/images/{dish['slug']}.svg"
        dish["image_source"] = "Hình minh hoạ tự tạo (SVG) - Demo"


async def seed_data() -> int:
    """Seed all demo data. Returns number of dishes inserted."""
    normalize_images()
    db_conn = await db.get_db()
    try:
        count_row = await db_conn.execute("SELECT COUNT(*) FROM dishes")
        count = (await count_row.fetchone())[0]
        if count >= len(DISHES):
            await db_conn.close()
            return count

        for dish in DISHES:
            restaurants = dish.pop("restaurants", [])
            recipe = dish.pop("recipe", None)
            reviews = dish.pop("reviews", [])

            await db_conn.execute(
                """INSERT INTO dishes (name, slug, description, meal_type, image_url, image_source,
                                      avg_rating, avg_price, is_demo, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)""",
                (
                    dish["name"],
                    dish["slug"],
                    dish["description"],
                    dish["meal_type"],
                    dish["image_url"],
                    dish["image_source"],
                    dish["avg_rating"],
                    dish["avg_price"],
                    datetime.utcnow().isoformat(),
                ),
            )
            row = await db_conn.execute("SELECT last_insert_rowid()")
            dish_id = (await row.fetchone())[0]

            for rest in restaurants:
                await db_conn.execute(
                    """INSERT INTO restaurants (dish_id, name, address, district, hours, price_range,
                                               maps_link, maps_source, is_demo)
                       VALUES (?, ?, ?, ?, ?, ?, ?, 'Demo - Chưa xác minh', 1)""",
                    (
                        dish_id,
                        rest["name"],
                        rest["address"],
                        rest["district"],
                        rest["hours"],
                        rest["price_range"],
                        build_maps_link(rest["name"], rest["address"]),
                    ),
                )

            if recipe:
                await db_conn.execute(
                    """INSERT INTO recipes (dish_id, ingredients, portions, cook_time, steps, source)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        dish_id,
                        json.dumps(recipe["ingredients"], ensure_ascii=False),
                        recipe["portions"],
                        recipe["cook_time"],
                        json.dumps(recipe["steps"], ensure_ascii=False),
                        recipe["source"],
                    ),
                )

            for rev in reviews:
                await db_conn.execute(
                    """INSERT INTO reviews (dish_id, rating, comment, reviewer_name, is_demo, created_at)
                       VALUES (?, ?, ?, ?, 1, ?)""",
                    (
                        dish_id,
                        rev["rating"],
                        rev["comment"],
                        rev["reviewer_name"],
                        (datetime.utcnow() - timedelta(days=random.randint(1, 90))).isoformat(),
                    ),
                )

        await db_conn.commit()
        return len(DISHES)
    finally:
        await db_conn.close()