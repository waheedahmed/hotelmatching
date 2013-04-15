import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from matching.models import *
from fuzzywuzzy import fuzz, process

hotel_path = 'hotels.dat'
match_path = 'matchInfo.dat'


def hotel_matching(request):
    ctx = dict()
    num = 1
    sug_count = 0
    irr_count = 0
    type = "suggestions"
    irrelevant_ids, matched_ids, confirmed_ids, confirmed_mids = getids()
    count = Matches.objects.count()
    if 'type' in request.GET:
        type = request.GET["type"]
    if 'page' in request.GET:
        num = int(request.GET['page'])
    if num <= count:
        matched_hotel = Matches.objects.exclude(mid__in=confirmed_mids)[num-1]
        matches_list = []
        suggestions_list = []
        if type == "suggestions":
            combined_list = list(irrelevant_ids)+list(matched_ids)+list(confirmed_ids)
        elif type == "irrelevant":
            combined_list = list(matched_ids)+list(confirmed_ids)
        for match in json.loads(matched_hotel.matches):
            ratio_count = getratio(matched_hotel, match)
            if "phone" in match and int(match["hid"]) not in irrelevant_ids and int(match["hid"]) not in matched_ids : sug_count+=1
            if "phone" in match and int(match["hid"]) in irrelevant_ids: irr_count+=1
            if ratio_count >= 2:
                match["color"] = "#ccff99"
            elif ratio_count == 1:
                match["color"] = "#ffffcc"
            else:
                match["color"] = "#ffcc99"
            if int(match['hid']) not in combined_list and type == "suggestions" and "phone" in match:
                suggestions_list.append(match)
            if int(match['hid']) in irrelevant_ids and type == "irrelevant" and "phone" in match:
                suggestions_list.append(match)
            if int(match['hid']) in list(matched_ids):
                matches_list.append(match)
        if 'color' in request.GET:
            new_list = []
            new_list2 = []
            for item in suggestions_list:
                if item["color"].lower() == "#%s"%request.GET["color"].lower() and "phone" in item: new_list.append(item)
                elif "phone" in item: new_list2.append(item)
            suggestions_list = new_list+new_list2
        ctx["json_list"] = suggestions_list
        ctx["matched"] = matched_hotel
        ctx["matched_list"] = matches_list
        ctx["cur_page"] = num
        ctx["type"] = type
        ctx["irr_count"] = irr_count
        ctx["sug_count"] = sug_count
        if num < count:
            ctx["next_page"] = num + 1
        if num > 0:
            ctx["prev_page"] = num - 1
    return render_to_response('matching.html', ctx, context_instance=RequestContext(request))


def irrelevant(request):
    MatchedID.objects.filter(MatchID=int(request.POST['irr_id'])).delete()
    irr_obj = Irrelevant()
    irr_obj.IrrelevantID = request.POST['irr_id']
    irr_obj.save()
    return HttpResponse(json.dumps({'msg': 'irrelevant added'}), mimetype="application/json")

def match(request):
    match_obj = MatchedID()
    match_obj.MatchID = request.POST['match_id']
    match_obj.save()
    Irrelevant.objects.filter(IrrelevantID=int(request.POST['match_id'])).delete()
    return HttpResponse(json.dumps({'msg': 'match added'}), mimetype="application/json")

def savematches(request):
    hids = request.POST.getlist("hids[]")
    mid = request.POST["mid"]
    for hid in hids:
        exist = ConfirmedMatched.objects.filter(mid=mid, hid=hid)
        if not exist:
            cnfrm_obj = ConfirmedMatched()
            cnfrm_obj.mid = int(mid)
            cnfrm_obj.hid = int(hid)
            cnfrm_obj.save()
    if not hids:
        cnfrm_obj = ConfirmedMatched()
        cnfrm_obj.mid = int(mid)
        cnfrm_obj.save()
    return HttpResponse(json.dumps({'msg': 'saved'}), mimetype="application/json")

def getids():
    irrelevant_ids = set()
    matched_ids = set()
    confirmed_ids = set()
    confirmed_mids = set()
    for irr in Irrelevant.objects.all():
        irrelevant_ids.add(irr.IrrelevantID)
    for ma in MatchedID.objects.all():
        matched_ids.add(ma.MatchID)
    for cid in ConfirmedMatched.objects.all():
        confirmed_ids.add(cid.hid)
        confirmed_mids.add(cid.mid)
    return irrelevant_ids, matched_ids, confirmed_ids, confirmed_mids

def getratio(matched_hotel, match):
    ratio_count = 0
    name_value = fuzz.partial_ratio(matched_hotel.name if matched_hotel.name else 'NONE', match["name"] if match["name"] else 'EMPTY')
    if name_value >= 85: ratio_count+=1
    add_value = fuzz.partial_ratio(matched_hotel.address if matched_hotel.address else 'NONE', match["addr"] if match["addr"] else 'EMPTY')
    if add_value >= 75: ratio_count+=1
    url_value = fuzz.partial_ratio(matched_hotel.url if matched_hotel.url else 'NONE', match["url"] if match["url"] else 'EMPTY')
    if url_value >= 85: ratio_count+=1
    phone_value = fuzz.partial_ratio(matched_hotel.phone if matched_hotel.phone else 'NONE', match["phone"] if 'phone' in match and match["phone"] else 'EMPTY')
    if phone_value >= 85: ratio_count+=1
    cords_value = fuzz.partial_ratio(matched_hotel.coordinates if matched_hotel.coordinates else 'NONE', match["cords"] if match["cords"] else 'EMPTY')
    if cords_value >= 75: ratio_count+=1
    return ratio_count

# def insert_matching():
#     dic = {}
#     hotels = get_hotel_dict()
#     counts = 0
#     with open(match_path, 'rU') as f:
#         for row in csv.reader(f, delimiter='\t'):
#             mdlobj = Matches()
#             mdlobj.mid = int(row[0].strip())
#             mdlobj.name = row[1].strip().decode("utf-8")
#             mdlobj.coordinates = '%s, %s' % (row[9].strip(), row[10].strip())
#             mdlobj.address = row[6].strip()
#             mdlobj.matches = json.dumps([get_match_object(hotels, i) for i in split(row[12].strip())])
#             mdlobj.url = row[-2].strip()
#             phone = row[8]
#             if 'null' not in phone:
#                 mdlobj.phone = phone.split('phone=')[1]
#             mdlobj.save()
#             counts += 1
#             print '===>> %s Saved, Total = %d' % (row[0], counts)
#
#
# def split(s):
#     ls = []
#     for row in s.split(' '):
#         ls.append(row.split(':')[0])
#     return ls
#
#
# def get_hotel_dict():
#     dic = {}
#     with open(hotel_path, 'rU') as f:
#         for row in csv.reader(f, delimiter='\t'):
#             if len(row) >= 11:
#                 dic[row[0]] = {'hid':row[0].strip(),'name':row[1].strip().decode("utf-8"),
#                                'addr':row[6].strip(),'cords':'%s, %s' % (row[9].strip(), row[10].strip()),
#                                'url':row[-1].strip(), 'phone': row[8]}
#     return dic
#
#
# def get_cords(dic, id):
#     if id in dic:
#         return dic[id]
#     else:
#         return ''
#
#
# def get_match_object(dic, id):
#     obj = {}
#     if id in dic:
#         return dic[id]
#     return {'hid': id, 'name': '', 'addr': '', 'cords': '', 'url': ''}